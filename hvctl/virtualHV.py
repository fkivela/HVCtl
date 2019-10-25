from virtualconnection import VirtualConnection
from message import Message


class VirtualHV(VirtualConnection):
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.voltage = 0
        self.current = 0
        self.HV_on_command = False
        self.HV_off_command = False
        self.HV_on_status = False
        self.interlock = False
        self.fault = False
        self.regulation = 'voltage'
    
    def get_voltage(self, _):
        return self.voltage
    
    def get_current(self, _):
        return self.current
    
    def set_voltage(self, value):
        self.voltage = value
        return self.voltage
    
    def set_current(self, value):
        self.current = value
        return self.current
        
    def HV_on(self, value):
        if value == self.HV_on_command:
            raise RuntimeError(f'*HV_on_command* is already {value}')
        
        if self.HV_on_command:
            self.HV_on_status = True
            
        self.HV_on_command = value
        return self.HV_on_command
            
    def HV_off(self, value):
        if value == self.HV_off_command:
            raise RuntimeError(f'*HV_off_command* is already {value}')
        
        if self.HV_off_command:
            self.HV_on_status = False
            
        self.HV_off_command = value
        return self.HV_off_command
    
    def mode(self, value):
        self.mode = 'local' if value else 'remote'
        return value
    
    def inhibit(self, value):
        self.inhibit = 'active' if value else 'idle'
        return value
    
    def status(self, _):
        values = [
            self.inhibit == 'active',
            self.mode == 'local',
            self.HV_off_command,
            self.HV_on_command,
            self.HV_on_status,
            self.interlock,
            self.fault,
            self.regulation == 'voltage']
        bits = ''.join([str(int(v)) for v in values])
        return int(bits, 2)
    
    def process(self, input_):
        message = Message.from_bytes(input_, is_answer=False)
        command = message.command        
        method = getattr(self, command.replace(' ', '_'))        
        
        ret = method(message.value)
        return Message(command, ret, is_answer=True).to_bytes()