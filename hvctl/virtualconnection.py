"""This module defines the :class:`VirtualConnection` class,
which can be used to simulate serial connections.
"""

import os
import pty
import select
import threading
import time

class VirtualConnection():
    """A virtual serial connection.

    Data can be sent through a :class:`VirtualConnection` object by
    accessing the :attr:`user_end` and :attr:`virtual_end` attributes.
    :attr:`virtual_end` can be written to and read from with
    :func:`os.read` and :func:`os.write`.
    :func:`os.read` doesn't seem to work with :attr:`user_end`,
    and the :mod:`serial` module should be used instead.
    :attr:`port` returns a device name which can be given to
    :func:`serial.Serial` as an argument.

    A :class:`VirtualConnection` object runs code in a parallel thread.
    If a VC is not closed after it is no longer needed,
    it may continue using resources needlessly.
    A VC may be closed by calling :func:`close`; this stops the
    parallel thread, closes :attr:`user_end` and :attr:`virtual_end`,
    and frees their file descriptors.

    If a VC is used with a ``with`` block in the following manner:

    .. code-block:: python

        with VirtualConnection as vc:
            # some code here

    the VC will close automatically when the ``with`` block is exited.

    It is possible for a VC to continue running even if there
    are no accessible references to it.
    This happens e.g. if a VC is
    defined in an IPython console and then deleted using ``del vc``.
    This deletes the name ``vc``, but doesn't seem to garbage-collect
    the object.
    In this case, all running instances of the
    :class:`VirtualConnection` class can be closed with

    >>> VirtualConnection.close_all()

    Attributes:
        buffer_size (int):
            The buffer size for the connection
            (how many bits are read at once).

        sleep_time (float):
            How long (in seconds) the object waits after checking for
            input before doing it again.

        process (function):
            The method used for processing input and forming output.
            Should have the same signature as :attr:`process`.

        virtual_end:
             A file-like object used by a simulated device to read
             and write data.

        user_end:
            A file-like object used by the UI to read and write data.

        thread (:class:`threading.Thread`):
            The parallel thread used to run a :class:`VirtualConnection`.

        running_instances:
            Class attribute.
            A set of all currently running instances of the
            :class:`VirtualConnection` class.
    """

    # Keep references to all running instances of this class.
    running_instances = set()

    def __init__(self, process=None, buffer_size=1024, sleep_time=0.01):
        """Initialize a new :class:`VirtualConnection`.

        The new instance starts running automatically.

        Args:
            process (function):
                The value of :attr:`process`.
                If no value is supllies, :atrr:`default_process`
                will be used.

            buffer_size:
                The value of :attr:`buffer_size`.

            sleep_time:
                The value of :attr:`sleep_time`.
        """
        if process:
            self.process = process
        else:
            self.process = self.default_process

        self.buffer_size = buffer_size
        self.sleep_time = sleep_time

        master, slave = pty.openpty()
        # This may be written to and read from with os.write
        # and os.read.
        self.virtual_end = master
        # os.read doesn't seem to work with this, but the serial
        # module does.
        self.user_end = slave

        # A parallel thread for the function self._run().
        self.thread = threading.Thread(target=self._run, args=[])
        # Daemon threads are killed when there are no more non-daemon
        # threads left. Setting daemon to True prevents the parallel
        # thread from running in the background even after the main
        # program has exited.
        self.thread.daemon = True

        # Flag for stopping the parallel thread.
        self._stop_flag = threading.Event()
        # Add this instance to the set.
        self.running_instances.add(self)
        self.thread.start()

    def __enter__(self):
        """Called at the beginning of a ``with`` block; returns
        *self*.
        """
        return self

    def __exit__(self, type_, value, traceback):
        """Called upon exiting a ``with`` block; calls
        :meth:`close`.
        """
        self.close()

    def close(self):
        """Stop the parallel thread and close the connection.

        This function returns only after the parallel thread has
        actually stopped.
        """
        if self.is_running():
            self._stop_flag.set()

        # Wait for the parallel thread to stop.
        while self.is_running():
            time.sleep(self.sleep_time)

        # Unlike set.remove(x), set.discard(x) doesn't raise an error
        # if there is no x in the set.
        self.running_instances.discard(self)

    @classmethod
    def close_all(cls):
        """Close all running instances of this class.

        This function returns only after all parallel threads have
        actually stopped.
        """
        # Iterate over a copy, because closing a VC removes it from
        # cls.running_instances, and removing members from a set
        # during iteration raises an error.
        copy = cls.running_instances.copy()
        for i in copy:
            i.close()

    def is_running(self):
        """Return ``True`` IFF the parallel thread is running."""
        return self.thread.is_alive()

    @property
    def port(self):
        """Return a device name (e.g. ``'/dev/pts/...'``) that can be
        used as the *port* argument when a :class:`serial.Serial`
        object is created."""
        return os.ttyname(self.user_end)

    def _run(self):
        """Run the parallel thread."""

        while not self._stop_flag.is_set():
            # If there is nothing to read from self.virtual_end,
            # os.read will block forever even with a timeout.
            # select makes sure this doesn't happen.
            ready_for_read, _, _ = select.select([self.virtual_end], [], [], 0)

            if self.virtual_end in ready_for_read:
                input_ = os.read(self.virtual_end, self.buffer_size)
            else:
                time.sleep(self.sleep_time)
                continue

            output = self.process(input_)
            os.write(self.virtual_end, output)

        # Close the files after the parallel thread has stopped.
        # Otherwise the system will run out of file descriptors,
        # if a VirtualConnection is created and stopped many times
        # in a a row.
        os.close(self.user_end)
        os.close(self.virtual_end)

    def default_process(self, input_): # pylint: disable=no-self-use
        """Form output based on *input_*.

        This is the default method assigned to :attr:`process`,
        and simply returns *input_* uncanged.

        Args:
            input_: A bytes-like object.

        Returns:
            *input_*.
        """
        # *self* is included as an argument since this may be
        # overridden by a method that uses *self*.

        output = input_
        return output
