Search.setIndex({docnames:["index","installation","modules/advanced_tui","modules/api","modules/command_line_ui","modules/config","modules/index","modules/message","modules/queuefile","modules/virtualconnection","modules/virtualhv","modules/widgets","protocol","usage"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,sphinx:56},filenames:["index.rst","installation.rst","modules/advanced_tui.rst","modules/api.rst","modules/command_line_ui.rst","modules/config.rst","modules/index.rst","modules/message.rst","modules/queuefile.rst","modules/virtualconnection.rst","modules/virtualhv.rst","modules/widgets.rst","protocol.rst","usage.rst"],objects:{"hvctl.advanced_tui":{AdvancedTUI:[2,1,1,""]},"hvctl.advanced_tui.AdvancedTUI":{__init__:[2,2,1,""],cli:[2,3,1,""],display:[2,3,1,""],keypress:[2,2,1,""],run:[2,2,1,""]},"hvctl.api":{API:[3,1,1,""],Status:[3,1,1,""]},"hvctl.api.API":{__enter__:[3,2,1,""],__exit__:[3,2,1,""],__init__:[3,2,1,""],full_status:[3,2,1,""],get_current:[3,2,1,""],get_status:[3,2,1,""],get_voltage:[3,2,1,""],halt:[3,2,1,""],hv_off:[3,2,1,""],hv_on:[3,2,1,""],run:[3,2,1,""],set_current:[3,2,1,""],set_inhibit:[3,2,1,""],set_mode:[3,2,1,""],set_voltage:[3,2,1,""],status:[3,3,1,""],timestep:[3,3,1,""]},"hvctl.api.Status":{__setattr__:[3,2,1,""],__str__:[3,2,1,""],callback:[3,3,1,""],current:[3,3,1,""],fault:[3,3,1,""],hv_off_command:[3,3,1,""],hv_on_command:[3,3,1,""],hv_on_status:[3,3,1,""],inhibit:[3,3,1,""],interlock:[3,3,1,""],mode:[3,3,1,""],regulation:[3,3,1,""],voltage:[3,3,1,""]},"hvctl.command_line_ui":{CommandLineUI:[4,1,1,""]},"hvctl.command_line_ui.CommandLineUI":{__enter__:[4,2,1,""],__exit__:[4,2,1,""],__init__:[4,2,1,""],api:[4,3,1,""],cmd_debug:[4,2,1,""],cmd_exit:[4,2,1,""],cmd_fullstatus:[4,2,1,""],cmd_getcurrent:[4,2,1,""],cmd_getvoltage:[4,2,1,""],cmd_help:[4,2,1,""],cmd_hvoff:[4,2,1,""],cmd_hvon:[4,2,1,""],cmd_inhibit:[4,2,1,""],cmd_mode:[4,2,1,""],cmd_setcurrent:[4,2,1,""],cmd_setvoltage:[4,2,1,""],cmd_status:[4,2,1,""],cmds_and_aliases:[4,3,1,""],debug:[4,3,1,""],indent:[4,3,1,""],input:[4,2,1,""],inputfile:[4,3,1,""],intro:[4,3,1,""],outputfile:[4,3,1,""],print:[4,2,1,""],prompt:[4,3,1,""],run:[4,2,1,""]},"hvctl.config":{CURRENT_LIMT:[5,3,1,""],DELTA_I:[5,3,1,""],DELTA_U:[5,3,1,""],INT_MAX:[5,3,1,""],SERIAL_KWARGS:[5,3,1,""],VOLTAGE_LIMIT:[5,3,1,""],main:[5,4,1,""]},"hvctl.message":{COMMANDS:[7,5,1,""],Message:[7,1,1,""]},"hvctl.message.Message":{ENCODING:[7,3,1,""],__init__:[7,2,1,""],__repr__:[7,2,1,""],command:[7,3,1,""],from_bytes:[7,2,1,""],is_answer:[7,3,1,""],value:[7,3,1,""]},"hvctl.queuefile":{QueueFile:[8,1,1,""]},"hvctl.queuefile.QueueFile":{__init__:[8,2,1,""],block:[8,3,1,""],flush:[8,2,1,""],queue:[8,3,1,""],read:[8,2,1,""],readline:[8,2,1,""],write:[8,2,1,""]},"hvctl.virtualconnection":{VirtualConnection:[9,1,1,""]},"hvctl.virtualconnection.VirtualConnection":{__enter__:[9,2,1,""],__exit__:[9,2,1,""],__init__:[9,2,1,""],buffer_size:[9,3,1,""],close:[9,2,1,""],close_all:[9,2,1,""],default_process:[9,2,1,""],is_running:[9,2,1,""],port:[9,2,1,""],process:[9,3,1,""],running_instances:[9,3,1,""],sleep_time:[9,3,1,""],thread:[9,3,1,""],user_end:[9,3,1,""],virtual_end:[9,3,1,""]},"hvctl.virtualhv":{VirtualHV:[10,1,1,""]},"hvctl.virtualhv.VirtualHV":{__enter__:[10,2,1,""],__exit__:[10,2,1,""],__init__:[10,2,1,""],connection:[10,3,1,""],current:[10,3,1,""],fault:[10,3,1,""],get_current:[10,2,1,""],get_status:[10,2,1,""],get_voltage:[10,2,1,""],hv_off:[10,2,1,""],hv_off_command:[10,3,1,""],hv_on:[10,2,1,""],hv_on_command:[10,3,1,""],hv_on_status:[10,3,1,""],inhibit:[10,3,1,""],interlock:[10,3,1,""],mode:[10,3,1,""],process:[10,2,1,""],regulation:[10,3,1,""],set_current:[10,2,1,""],set_inhibit:[10,2,1,""],set_mode:[10,2,1,""],set_voltage:[10,2,1,""],voltage:[10,3,1,""]},"hvctl.widgets":{CLI:[11,1,1,""],CommandHistory:[11,1,1,""],CommandLines:[11,1,1,""],Position:[11,1,1,""],ScrollBar:[11,1,1,""],ScrollButton:[11,1,1,""],ScrollableWidget:[11,1,1,""]},"hvctl.widgets.CLI":{__init__:[11,2,1,""],arrow_down:[11,3,1,""],arrow_up:[11,3,1,""],cmdlines:[11,3,1,""],position:[11,3,1,""],scrollable_lines:[11,3,1,""],scrollbar:[11,3,1,""]},"hvctl.widgets.CommandHistory":{__init__:[11,2,1,""],down:[11,2,1,""],enter_command:[11,2,1,""],get_command:[11,2,1,""],history:[11,3,1,""],index:[11,3,1,""],temp_history:[11,3,1,""],up:[11,2,1,""],update_command:[11,2,1,""]},"hvctl.widgets.CommandLines":{__init__:[11,2,1,""],edit:[11,3,1,""],enter:[11,2,1,""],history:[11,3,1,""],history_down:[11,2,1,""],history_up:[11,2,1,""],input_queue:[11,3,1,""],keypress:[11,2,1,""],move_cursor_to_end:[11,2,1,""],output_queue:[11,3,1,""],update:[11,2,1,""]},"hvctl.widgets.Position":{__init__:[11,2,1,""],absolute:[11,3,1,""],listeners:[11,3,1,""],max_absolute:[11,2,1,""],relative:[11,3,1,""],total_rows:[11,3,1,""],visible_rows:[11,3,1,""]},"hvctl.widgets.ScrollBar":{__init__:[11,2,1,""],background_char:[11,3,1,""],mouse_event:[11,2,1,""],position:[11,3,1,""],render:[11,2,1,""]},"hvctl.widgets.ScrollButton":{__init__:[11,2,1,""],mouse_event:[11,2,1,""],position:[11,3,1,""],step:[11,3,1,""]},"hvctl.widgets.ScrollableWidget":{__init__:[11,2,1,""],keypress:[11,2,1,""],mouse_event:[11,2,1,""],position:[11,3,1,""],render:[11,2,1,""],widget:[11,3,1,""]},hvctl:{advanced_tui:[2,0,0,"-"],api:[3,0,0,"-"],command_line_ui:[4,0,0,"-"],config:[5,0,0,"-"],message:[7,0,0,"-"],queuefile:[8,0,0,"-"],virtualconnection:[9,0,0,"-"],virtualhv:[10,0,0,"-"],widgets:[11,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","function","Python function"],"5":["py","data","Python data"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:function","5":"py:data"},terms:{"10kw":[],"5kw":12,"boolean":3,"break":4,"byte":[7,9,10],"case":[3,9],"char":11,"class":[2,3,4,6,7,8,9,10,11,13],"default":[4,9],"float":[3,9,10,11],"function":[3,4,5,9,11,12],"import":[0,5,6],"int":[7,9,10,11],"kivel\u00e4":0,"long":9,"mets\u00e4":0,"new":[1,2,3,4,7,8,9,10,11],"public":0,"return":[2,3,4,7,8,9,10,11,12],"static":[4,9],"switch":[3,13],"true":[3,4,5,7,8,9,10,11],"while":11,FOR:0,For:[5,7,12],Has:4,Its:[3,9],The:[0,3,4,5,7,8,9,10,11,12,13],These:[10,13],Use:2,__enter__:[3,4,9,10],__exit__:[3,4,9,10],__init__:[2,3,4,6,7,8,9,10,11],__repr__:7,__setattr__:3,__str__:3,a1x:12,a2x:12,about:3,abov:[11,13],absolut:11,accept:[4,11,13],access:[1,9,10,13],action:3,activ:[3,4,10],actual:[7,9],add:11,added:1,addit:1,advanc:13,advanced_tui:[0,6],advancedtui:2,after:[2,3,4,9,12],again:[4,9],algorithm:4,alia:4,alias:4,all:[3,4,6,7,8,9,11,12,13],allow:13,along:0,alreadi:[],also:[3,5,6,11,13],alwai:[3,8,11],among:11,amount:[5,11],ani:[0,11,12],anoth:[1,4],answer:[0,7],api:[0,4,6],apiobj:[],append:12,applic:5,arg:[10,13],argument:[3,4,5,7,8,9,11,13],arrow:[11,13],arrow_down:11,arrow_up:11,ascii:12,ask:4,assign:9,associ:7,attempt:7,attribut:[3,4,7,9,10,11],attributeerror:8,automat:[3,5,9,12],back:[3,10],background:4,background_char:11,bar:[11,13],base:[0,2,5,9,12],baud:12,baudrat:5,been:13,befor:[9,12],begin:[9,11],behaviour:[8,11],being:[3,11,12],below:[2,11,12,13],between:[3,7,8,11],big:[10,12],bit:[5,9,10,12],block:[3,4,8,9,10,13],bool:[3,4,7,8,10],both:[3,12,13],bottom:[11,13],box:11,brows:11,buffer:9,buffer_s:9,built:4,button:[11,13],bytes:5,bytes_:7,call:[2,3,4,5,9,10,13],callback:3,can:[0,1,2,3,5,7,8,9,10,11,13],cannot:[3,5],canva:11,carriag:12,caught:4,chang:[2,3,5,10,11],charact:[8,11,12],check:9,choos:1,classmethod:[7,9],classnam:7,cli:[2,11],click:[11,13],close:[3,4,9,10,12,13],close_al:9,cmd_:4,cmd_debug:4,cmd_exit:4,cmd_fullstatu:4,cmd_getcurr:4,cmd_getvoltag:4,cmd_help:4,cmd_hvoff:4,cmd_hvon:4,cmd_inhibit:4,cmd_mode:4,cmd_setcurr:4,cmd_setvoltag:4,cmd_statu:4,cmdline:11,cmds_and_alias:4,code:[9,13],col:11,collect:9,combin:2,comma:12,command:[0,2,3,4,7,10,11,13],command_line_ui:[0,6],commandhistori:11,commandlin:11,commandlineui:[2,4],commun:[3,7,10,12],comput:7,conf:[5,13],config:[0,6],configur:[0,5],connect:[3,7,9,10,12,13],consecut:11,consist:12,consol:9,constant:5,consum:4,contact:0,contain:[3,4,8,10,11,13],content:[2,3,11],continu:[4,9],control:[0,2,3,8,10,13],convers:7,copi:[0,10,12],copyright:0,correspond:[3,12],count:11,cover:12,crash:4,creat:[3,4,5,7,8,9,10,11,13],current:[3,4,5,7,9,10,11,13],current_limt:5,cursor:11,data:[3,9,12],deactiv:[3,4],debug:4,decreas:11,default_process:9,defin:[2,3,4,5,7,8,9,10,13],del:9,delet:9,delta_i:[5,7],delta_u:[5,7],demonstr:13,denot:12,depend:[0,3,7],describ:[4,10],descriptor:9,detail:[0,1,3,4,5],determin:[3,7,10],dev:9,develop:0,devic:[3,5,9,10,12,13],dict:[3,5],differ:[8,12,13],directli:12,directori:[0,5,13],disabl:4,displai:[2,3,4,11],displi:4,distribut:0,docstr:3,document:[5,13],doe:[3,8],doesn:[1,3,4,9,12,13],doing:9,don:12,done:[3,11],down:11,download:1,draw:11,dsrdtr:5,duplex:12,dure:4,each:4,earlier:0,easier:[4,8],easili:[8,13],edg:11,edit:[4,11],either:0,empti:11,emul:[8,11],enabl:4,encod:7,encount:8,end:[4,11,12,13],endian:[10,12],enet:11,ensu:3,ensur:13,enter:[3,4,10,11,12],enter_command:11,entri:11,equal:[10,11],error:[3,4],etc:11,evalu:[3,4],even:[0,9],event:11,everi:[3,4],exampl:[0,12],exc_typ:3,exc_valu:3,exceed:5,except:3,exception_typ:4,exception_valu:4,exclud:[4,10],exclus:5,execut:[4,10],exist:[4,8],exit:[2,3,4,9,10,13],fals:[3,4,7,8,10,11,13],falu:4,far:11,fault:[3,10,12,13],felik:0,field:2,file:[2,4,5,8,9,13],filenotfounderror:5,fill:11,first:[10,12],firstnam:0,fit:0,flag:8,flush:8,focu:11,follow:[4,5,9,10,12,13],form:[3,9,11],format:7,found:5,foundat:0,free:[0,9],from:[3,4,7,8,9,10,11,13],from_byt:[7,10],full:[4,12],full_statu:3,fullstatu:4,further:5,fusor:0,garbag:9,gener:[0,3,7,10,12],get:[3,4,7,10,11],get_command:11,get_curr:[3,10],get_statu:[3,10],get_voltag:[3,10,13],getcurr:4,geti:4,getter:7,getu:4,getvoltag:[4,13],give:11,given:[3,4,7,8,9,11,12,13],gnu:0,ground:12,halt:[3,4,13],handl:[2,10,11],happen:[8,9],has:[2,9,10,12],hasn:13,have:[0,9,13],height:11,help:[4,13],helsinki:0,here:[9,11,12,13],high:[0,10],histori:11,history_down:11,history_up:11,hope:0,how:[9,11,12],http:0,hv_off:[3,10],hv_off_command:[3,10],hv_on:[3,10],hv_on_command:[3,10],hv_on_statu:[3,10],hvctl:[2,3,4,5,6,7,8,9,10,11,13],hvoff:4,hvon:4,ident:[11,13],idl:12,iff:[9,10],ignor:[4,10],impli:0,inact:4,includ:[1,3,4,5,8,10,11,13],increas:11,indent:4,index:[4,11],indic:8,inform:[2,3],inhibit:[3,4,7,10],initi:[2,3,4,9,10,11],input:[2,4,8,9,10,11],input_:[9,10],input_queu:11,inputfil:[2,4,11],insid:3,instal:[0,2,13],instanc:[3,4,9,13],instead:[4,9,10,11,13],instruct:12,int_max:[5,7],integ:[5,10,12],intend:0,interact:0,interfac:[1,2,8,11,13],interlock:[3,10,12,13],interpret:13,intial:8,intro:4,invalid:[4,7],invis:11,ipython:9,is_answ:7,is_run:9,isn:2,issu:2,iter:[4,11],its:[2,4,7,8,11,12,13],keep:[11,13],kei:[2,3,11],keypress:[2,11],keyword:5,last:13,lastnam:0,later:[0,5],latter:13,launch:13,least:12,left:[7,11,12],lenger:3,length:11,less:8,letter:12,librari:[1,11],like:[2,4,6,8,9,10,11],likk:[],line:[2,4,11,13],linearli:12,linux:[0,11],list:[0,4,6,7,11,13],listen:11,local:[3,4,10,13],locat:[1,2,5,11,13],longer:[3,4,9],loop:[2,4],lost:3,lsb:12,made:[1,7],mai:[4,9,12,13],main:5,make:[4,8,10,11,13],mani:9,manner:[9,10,12],match:3,matter:3,max_absolut:11,maximum:[5,11,12],mean:12,member:13,memori:11,merchant:0,messag:[0,3,4,6,10,13],meth:8,method:[3,4,8,9,10,11,13],mode:[0,3,4,7,10],modifi:[0,11],modul:[0,2,3,4,5,7,8,9,10,11,13],more:[0,3,12,13],most:[6,12],mous:[11,13],mouse_ev:11,move:11,move_cursor_to_end:11,msb:12,multipl:11,multipli:7,must:1,name:[3,4,5,9],namespac:[6,13],need:[3,4,6,9],needlessli:9,neg:[5,11,12],never:[5,8],newer:11,newest:11,newlin:8,next:13,none:[3,4,7,8,9,11],normal:3,noth:[8,11],number:[8,10,11,12],numer:12,object:[2,3,4,5,7,8,9,10,11,13],occur:3,off:[3,4,7,10,13],old:[10,11],older:11,oldest:11,onc:9,one:[8,11,12,13],ones:[],onli:[4,9,11],open:[3,12],openpti:8,oper:0,option:[0,5],order:[1,3,10],org:0,origin:11,other:11,otherwis:[3,4,10,11],output:[2,4,8,9,11],output_queu:11,outputfil:[2,4,11],over:11,own:13,packag:[1,6,13],page:[6,13],pair:12,parallel:[2,3,4,9,13],paramet:[2,3,4,9,10,11,12],pariti:[5,12],pars:[4,5,10],part:[8,11,13],particular:[0,5],pass:[4,10],path:1,pekko:0,perform:[3,11],physic:[10,13],point:11,polar:[3,5,12],poll:[3,13],port:[3,4,5,9,13],posit:[3,11],possibl:[8,9,10,11,13],potenti:12,power:13,present:[2,3,10,12,13],press:[2,11,13],prevent:[3,4],previou:11,previous:11,print:[2,4,8,11],process:[9,10,11],process_command:11,produc:[3,11],program:[0,2,4,8,11],programmat:13,prompt:4,properli:[3,13],properti:[7,9,11],protocol:[0,5],provid:[2,4,11,13],psu:[3,4,7,10,12],pts:9,pty:8,publish:0,purpos:0,pyseri:1,python:[0,1,6,10,12,13],pythonpath:1,question:12,queue:[8,11],queuefil:[0,6],rais:[3,4,5,7,8,10],rang:[7,10,12],rate:12,read:[8,9,11,13],readi:0,readlin:[4,8],real:13,receiv:[0,3,4,7,12],recogn:12,redirect:8,redistribut:0,refer:9,regardless:3,regul:[3,10,12,13],rel:[1,11],remot:[3,4,10,13],render:11,repli:3,report:3,repres:[7,12],request:[4,11],requir:13,reset:11,resourc:[4,9],respect:10,respons:7,result:13,right:12,routin:3,row:11,rtsct:5,run:[1,2,3,4,9,13],running_inst:9,runtimeerror:[3,5,10],safe:8,same:[3,5,8,10,11,13],save:[8,11],scale:12,screen:[2,11,13],script:[1,2,13],scroll:[11,13],scrollabl:11,scrollable_lin:11,scrollablewidget:11,scrollbar:11,scrollbutton:11,scroller:11,scroller_char:11,second:[3,9,12],section:12,see:[0,1,3,4,5,13],seem:9,select:11,self:[3,4,7,9,10,11],send:[3,4,7,12,13],sent:[2,3,7,9],sep:4,separ:12,serial:[3,5,7,9,10,13],serial_kwarg:[3,5],set:[3,4,5,7,8,9,10,11,13],set_curr:[3,10],set_inhibit:[3,10],set_mod:[3,10],set_text:2,set_voltag:[3,10,13],setcurr:4,seti:4,setu:4,setvoltag:[4,13],sever:5,share:11,shortcut:13,shorter:13,should:[0,1,2,3,4,5,7,8,9,11],show:13,sign:3,signatur:9,signific:12,simpl:[4,13],simpler:1,simpli:[1,9,13],simul:[9,10,13],sinc:[3,6,10],singl:[11,12],size:[2,8,9,11],skip:3,sleep_tim:9,slighlti:13,slightli:13,smallest:5,softwar:0,some:9,sould:3,specif:12,specifi:4,split:4,sr100kv:12,standard:[1,8,11],start:[2,3,4,9,12],statu:[3,4,7,10,13],stdin:4,stdout:4,step:[4,11],stop:[3,8,9,12],stopbit:5,store:[3,11],str:[3,11],string:[4,7,8,10,11,12],stringio:8,style:2,suitabl:3,suplli:9,symbol:11,syntax:[],sys:4,system:0,tabl:12,taken:[],task:11,team:0,technix:[0,3],temp_histori:11,term:0,termin:[2,11],test:[1,10,13],text:[2,4,11],textiobas:8,than:[8,11],thei:[4,6,13],them:12,thi:[0,2,3,4,5,6,7,8,9,10,11,12,13],those:[3,8,11],thread:[2,3,4,8,9,13],through:[7,9,10,11],time:[3,4,8],timeout:5,timestep:3,to_byt:10,top:[11,13],total_row:11,traceback:[3,4,9,10],track:11,tui:[2,3,11],tupl:4,turn:[3,4,10],two:13,type:[2,3,4,7,8,9,10,11,13],type_:[9,10],typeerror:4,uncang:9,under:0,univers:0,unsign:[5,12],updat:[3,11],update_command:11,upon:[3,4,9,10],upward:11,urwid:[1,2,11,13],usag:[0,1],used:[3,4,7,9,10,11,13],useful:0,user:[1,2,4,6,11],user_end:9,uses:[1,2,4,5,11,13],using:[1,4,8,9,13],utf:7,valid:[3,7],valu:[3,4,5,7,8,9,10,11,12],valueerror:[3,4,7],version:[0,1,5],vertic:11,vhv:13,view:11,virtual:[9,10],virtual_end:9,virtualconnect:[0,6,10],virtualhv:[0,6,13],visibl:11,visible_row:11,voltag:[0,3,4,5,7,10,13],voltage_limit:5,wait:[4,9,12],warranti:0,welcom:[4,13],well:13,whatev:11,wheel:[11,13],when:[2,4,5,7,9,11],whenev:[3,11],where:[2,4],whether:[3,7,8,10],which:[3,5,7,9,11,12],whitespac:4,whole:12,whose:12,widget:[0,6],width:11,without:[0,1,2,8,10,12],work:[0,1,4,9],would:8,wrap:[8,11],write:[4,8,9,11],written:[0,1,8,9,11],www:0,xonxoff:5,xyz:[],yet:0,you:0,your:[0,1]},titles:["HVCtl","Installation","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">advanced_tui</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">api</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">command_line_ui</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">config</span></code>","Modules","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">message</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">queuefile</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">virtualconnection</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">virtualhv</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">widgets</span></code>","RS-232 Control Protocol","Usage"],titleterms:{"import":13,"switch":12,The:1,Using:13,__init__:[],activ:12,advanced_tui:2,answer:12,api:[3,13],author:0,between:12,command:12,command_line_ui:4,config:5,configur:13,control:12,current:12,deactiv:12,depend:1,directori:1,document:0,exampl:13,get:12,hvctl:[0,1],inhibit:12,instal:1,interact:13,licens:0,list:12,local:12,messag:7,mode:[12,13],modul:6,off:12,output:12,power:12,protocol:12,psu:13,queuefil:8,remot:12,set:12,statu:12,suppli:12,turn:12,usag:13,virtual:13,virtualconnect:9,virtualhv:10,voltag:12,widget:11,without:13}})