Search.setIndex({docnames:["index","installation","modules/advanced_tui","modules/api","modules/command_line_ui","modules/config","modules/index","modules/message","modules/queuefile","modules/status_format","modules/virtualconnection","modules/virtualhv","modules/widgets","protocol","usage"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.intersphinx":1,sphinx:56},filenames:["index.rst","installation.rst","modules/advanced_tui.rst","modules/api.rst","modules/command_line_ui.rst","modules/config.rst","modules/index.rst","modules/message.rst","modules/queuefile.rst","modules/status_format.rst","modules/virtualconnection.rst","modules/virtualhv.rst","modules/widgets.rst","protocol.rst","usage.rst"],objects:{"hvctl.advanced_tui":{AdvancedTUI:[2,1,1,""]},"hvctl.advanced_tui.AdvancedTUI":{__init__:[2,2,1,""],command_line_interface:[2,3,1,""],display:[2,3,1,""],run:[2,2,1,""]},"hvctl.api":{API:[3,1,1,""],Status:[3,1,1,""]},"hvctl.api.API":{__enter__:[3,2,1,""],__exit__:[3,2,1,""],__init__:[3,2,1,""],full_status:[3,2,1,""],get_current:[3,2,1,""],get_status:[3,2,1,""],get_voltage:[3,2,1,""],halt:[3,2,1,""],hv_off:[3,2,1,""],hv_on:[3,2,1,""],set_current:[3,2,1,""],set_inhibition:[3,2,1,""],set_mode:[3,2,1,""],set_voltage:[3,2,1,""],status:[3,3,1,""],timestep:[3,3,1,""]},"hvctl.api.Status":{__setattr__:[3,2,1,""],callback:[3,3,1,""],current:[3,3,1,""],fault:[3,3,1,""],hv_off_command:[3,3,1,""],hv_on_command:[3,3,1,""],hv_on_status:[3,3,1,""],inhibition:[3,3,1,""],interlock:[3,3,1,""],mode:[3,3,1,""],regulation:[3,3,1,""],voltage:[3,3,1,""]},"hvctl.command_line_ui":{CommandLineUI:[4,1,1,""]},"hvctl.command_line_ui.CommandLineUI":{__enter__:[4,2,1,""],__exit__:[4,2,1,""],__init__:[4,2,1,""],api:[4,3,1,""],cmd_debug:[4,2,1,""],cmd_exit:[4,2,1,""],cmd_fullstatus:[4,2,1,""],cmd_getcurrent:[4,2,1,""],cmd_getvoltage:[4,2,1,""],cmd_help:[4,2,1,""],cmd_hv:[4,2,1,""],cmd_inhibit:[4,2,1,""],cmd_mode:[4,2,1,""],cmd_setcurrent:[4,2,1,""],cmd_setvoltage:[4,2,1,""],cmd_status:[4,2,1,""],cmds_and_aliases:[4,3,1,""],debug:[4,3,1,""],indent:[4,3,1,""],input:[4,2,1,""],inputfile:[4,3,1,""],intro:[4,3,1,""],outputfile:[4,3,1,""],print:[4,2,1,""],prompt:[4,3,1,""],run:[4,2,1,""]},"hvctl.config":{CURRENT_LIMIT:[5,3,1,""],DELTA_I:[5,3,1,""],DELTA_U:[5,3,1,""],INT_MAX:[5,3,1,""],SERIAL_KWARGS:[5,3,1,""],VOLTAGE_LIMIT:[5,3,1,""],load:[5,4,1,""]},"hvctl.message":{Message:[7,1,1,""]},"hvctl.message.Message":{ENCODING:[7,3,1,""],__bytes__:[7,2,1,""],__init__:[7,2,1,""],__repr__:[7,2,1,""],command:[7,3,1,""],from_bytes:[7,2,1,""],is_answer:[7,3,1,""],value:[7,3,1,""]},"hvctl.queuefile":{QueueFile:[8,1,1,""]},"hvctl.queuefile.QueueFile":{__init__:[8,2,1,""],block:[8,3,1,""],flush:[8,2,1,""],queue:[8,3,1,""],read:[8,2,1,""],readline:[8,2,1,""],write:[8,2,1,""]},"hvctl.status_format":{green_button:[9,3,1,""],palette:[9,3,1,""],red_button:[9,3,1,""],status_screen:[9,4,1,""],status_string:[9,4,1,""]},"hvctl.virtualconnection":{VirtualConnection:[10,1,1,""]},"hvctl.virtualconnection.VirtualConnection":{__enter__:[10,2,1,""],__exit__:[10,2,1,""],__init__:[10,2,1,""],buffer_size:[10,3,1,""],close:[10,2,1,""],close_all:[10,2,1,""],default_process:[10,2,1,""],is_running:[10,2,1,""],port:[10,2,1,""],process:[10,3,1,""],running_instances:[10,3,1,""],sleep_time:[10,3,1,""],thread:[10,3,1,""],user_end:[10,3,1,""],virtual_end:[10,3,1,""]},"hvctl.virtualhv":{VirtualHV:[11,1,1,""]},"hvctl.virtualhv.VirtualHV":{__enter__:[11,2,1,""],__exit__:[11,2,1,""],__init__:[11,2,1,""],close_interlock:[11,2,1,""],connection:[11,3,1,""],get_current:[11,2,1,""],get_status:[11,2,1,""],get_voltage:[11,2,1,""],hv_off:[11,2,1,""],hv_on:[11,2,1,""],open_interlock:[11,2,1,""],process:[11,2,1,""],refresh_watchdog:[11,2,1,""],reset_fault:[11,2,1,""],set_current:[11,2,1,""],set_inhibition:[11,2,1,""],set_mode:[11,2,1,""],set_voltage:[11,2,1,""],status:[11,3,1,""],time_of_last_command:[11,3,1,""]},"hvctl.widgets":{CommandHistory:[12,1,1,""],CommandLines:[12,1,1,""],Position:[12,1,1,""],ScrollBar:[12,1,1,""],ScrollButton:[12,1,1,""],ScrollableCommandLines:[12,1,1,""],Scroller:[12,1,1,""]},"hvctl.widgets.CommandHistory":{__init__:[12,2,1,""],down:[12,2,1,""],enter_command:[12,2,1,""],get_command:[12,2,1,""],history:[12,3,1,""],index:[12,3,1,""],temp_history:[12,3,1,""],up:[12,2,1,""],update_command:[12,2,1,""]},"hvctl.widgets.CommandLines":{__init__:[12,2,1,""],edit:[12,3,1,""],enter:[12,2,1,""],history:[12,3,1,""],history_down:[12,2,1,""],history_up:[12,2,1,""],inputfile:[12,3,1,""],keypress:[12,2,1,""],move_cursor_to_end:[12,2,1,""],outputfile:[12,3,1,""],update:[12,2,1,""]},"hvctl.widgets.Position":{__init__:[12,2,1,""],absolute:[12,3,1,""],listeners:[12,3,1,""],max_absolute:[12,2,1,""],relative:[12,3,1,""],total_rows:[12,3,1,""],visible_rows:[12,3,1,""]},"hvctl.widgets.ScrollBar":{__init__:[12,2,1,""],background_char:[12,3,1,""],mouse_event:[12,2,1,""],position:[12,3,1,""],render:[12,2,1,""],scroller_char:[12,3,1,""]},"hvctl.widgets.ScrollButton":{__init__:[12,2,1,""],mouse_event:[12,2,1,""],position:[12,3,1,""],step:[12,3,1,""]},"hvctl.widgets.ScrollableCommandLines":{__init__:[12,2,1,""],arrow_down:[12,3,1,""],arrow_up:[12,3,1,""],command_lines:[12,3,1,""],position:[12,3,1,""],scrollbar:[12,3,1,""],scroller:[12,3,1,""]},"hvctl.widgets.Scroller":{__init__:[12,2,1,""],keypress:[12,2,1,""],mouse_event:[12,2,1,""],position:[12,3,1,""],render:[12,2,1,""],widget:[12,3,1,""]},hvctl:{advanced_tui:[2,0,0,"-"],api:[3,0,0,"-"],command_line_ui:[4,0,0,"-"],config:[5,0,0,"-"],message:[7,0,0,"-"],queuefile:[8,0,0,"-"],status_format:[9,0,0,"-"],virtualconnection:[10,0,0,"-"],virtualhv:[11,0,0,"-"],widgets:[12,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","attribute","Python attribute"],"4":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:attribute","4":"py:function"},terms:{"5kw":[0,3,13],"boolean":3,"break":4,"byte":[7,10,11],"case":[10,13],"catch":4,"class":[2,3,4,6,7,8,10,11,12,14],"default":[3,4,5,10,14],"final":[2,11],"float":[3,10,11,12],"function":[3,4,5,10,11,12,13,14],"import":[0,5,6],"int":[3,7,10,11,12],"kivel\u00e4":0,"long":10,"mets\u00e4":0,"new":[1,2,3,4,7,8,10,11,12,13],"public":0,"return":[3,4,7,8,9,10,11,12,13],"static":[4,10],"switch":[3,11,14],"true":[3,4,5,7,8,10,11,12],"try":2,"while":[12,13],FOR:0,For:[7,13],Its:[3,10],The:[0,2,3,4,5,7,8,9,10,11,12,13,14],These:[4,11,14],UIs:9,Use:2,__bytes__:[7,11],__enter__:[3,4,10,11],__exit__:[3,4,10,11],__init__:[2,3,4,6,7,8,10,11,12],__main__:14,__repr__:7,__setattr__:3,a1x:13,a2x:13,about:3,abov:[12,14],absolut:[12,13,14],accept:[4,7,14],access:[1,10,11,14],action:[3,14],activ:[3,4],actual:[7,10,13,14],add:12,added:[1,14],addit:1,addition:14,advanc:14,advanced_tui:[0,6],advancedtui:[2,9],affect:14,after:[3,4,7,10,13],again:[4,10],algorithm:4,alia:4,alias:4,all:[3,4,6,7,8,10,12,13,14],allow:14,along:0,alreadi:11,also:[0,3,4,5,6,10,11,12,14],altern:1,alwai:[3,8,12],among:12,amount:[5,12],analog:5,ani:[0,4,11,12,13,14],anoth:[1,4,12,13,14],answer:[0,7],api:[0,4,6,9],append:13,appli:13,applic:5,approxim:12,arg:[11,14],argument:[4,5,7,8,10,12,14],arrow:[12,14],arrow_down:12,arrow_up:12,ascii:13,ask:4,assign:10,associ:7,attribut:[3,4,7,10,11,12],attributeerror:8,automat:[2,3,5,10,11,12,13,14],back:[3,13,14],background:4,background_char:12,bar:[12,14],base:[0,2,5,10,12,13],basescreen:2,baud:13,baudrat:5,beak:2,becaus:[4,14],been:[2,12,13,14],befor:[10,13,14],begin:10,behaviour:[8,12],being:[3,12,13],below:[2,12,13,14],between:[3,7,8,11,12],big:11,bit:[5,10,11],block:[2,3,4,8,10,11,14],bool:[3,4,7,8,11],both:[3,13,14],bottom:[12,14],box:12,brows:[12,14],buffer:10,buffer_s:10,built:[2,4],button:[11,12,13,14],bytes:5,bytes_:7,call:[2,3,4,5,10,11,12,14],callabl:[2,3],callback:3,can:[0,1,3,4,5,7,8,10,11,12,13,14],cannot:[3,4,5,13],canva:12,carriag:13,caught:4,caus:13,chang:[2,3,5,7,12],charact:[8,12,13],check:10,choos:1,circl:9,circuit:13,classmethod:[7,10],classnam:7,click:[12,14],close:[2,3,4,10,11,13,14],close_al:10,close_interlock:11,cmd_:4,cmd_command:4,cmd_debug:4,cmd_exit:4,cmd_fullstatu:4,cmd_getcurr:4,cmd_getvoltag:4,cmd_help:4,cmd_hv:4,cmd_inhibit:4,cmd_mode:4,cmd_setcurr:4,cmd_setvoltag:4,cmd_statu:4,cmds_and_alias:4,code:[2,10,14],col:12,colour:9,combin:2,comma:13,command:[0,2,3,4,7,10,11,12,14],command_lin:12,command_line_interfac:2,command_line_ui:[0,6],commandhistori:12,commandlin:12,commandlineui:[2,4],commun:[2,3,7,10,11,13,14],compar:11,comput:[5,7],condit:[11,13],conf:[5,14],config:[0,6,14],configur:[5,14],connect:[3,7,10,11,13,14],connector:13,consecut:12,consist:[12,13],constant:5,consum:4,contact:0,contain:[4,8,11,12,14],content:[2,3,9],continu:[4,10],control:[0,2,3,8,9,14],convers:[7,13],convert:[7,11],copi:[0,11,13],copyright:0,correct:5,correspond:[3,4,13],count:12,cover:13,crash:[2,4],creat:[3,4,5,7,8,10,11,12,14],current:[3,4,5,7,10,11,12,14],current_limit:5,cursor:12,data:[3,9,10,13],deactiv:[3,4],debug:4,decim:13,decreas:12,default_process:10,defin:[2,3,4,5,7,8,10,11,12,14],del:10,delai:13,delta_i:[5,7],delta_u:[5,7],demonstr:14,denot:13,depend:[0,3],describ:[0,4,11,13],descriptor:10,desir:13,detail:[0,1,3,4,5,11],determin:[3,7,13],dev:[10,14],develop:0,devic:[3,10,11,13],dict:[3,5],dictionari:9,differ:[5,8,11,12,13,14],directli:13,directori:[0,5,14],disabl:[4,14],displai:[2,3,4,9,12,13,14],distribut:0,divid:5,docstr:[3,4,12],document:[2,5,14],doe:[3,8],doesn:[1,3,4,10,11,13,14],doing:10,done:[3,12,14],down:[12,14],download:1,draw:12,dsrdtr:5,duplex:13,dure:4,each:[4,12,13,14],earlier:0,easier:[4,8],easili:[4,8,14],edg:12,edit:[4,12,14],effect:12,either:0,elaps:11,empti:12,emul:[8,11,12],enabl:14,encod:7,encount:8,end:[2,4,10,12,13,14],endian:11,ensur:14,enter:[2,3,4,11,12,13],enter_command:12,entir:13,entri:[2,12],equal:[11,12],error:[4,13],etc:12,evalu:3,even:[0,13],event:12,everi:[3,4,11,14],exampl:[0,2,13],exc_typ:3,exc_valu:3,exceed:5,exception_typ:4,exception_valu:4,exclud:[4,11,13],exclus:5,execut:[2,4,11],exist:[4,8],exit:[2,3,4,10,11,14],explain:[9,12,13],fals:[3,4,7,8,10,11,12,14],far:12,fault:[3,11,14],felik:0,field:2,file:[2,4,5,8,10,12,14],filenam:5,filenotfounderror:5,fill:14,first:[11,13],firstnam:0,fit:0,fix:12,flag:8,flow:12,flush:[4,8],focu:12,follow:[4,5,7,10,11,13,14],form:[3,4,10,12],format:[2,7,9],found:5,foundat:0,four:4,free:[0,10],from:[2,3,4,7,8,10,11,12,13,14],from_byt:[7,11],front:[11,13],full:[4,13],full_statu:[3,9],fullstatu:4,further:[5,11],fusor:0,gener:[0,3,4,5,7,9,11,12],get:[3,4,7,11,12],get_command:12,get_curr:[3,11],get_statu:[3,9,11],get_voltag:[3,11,14],getcurr:4,geti:4,getter:7,getu:4,getvoltag:[4,14],give:[4,12],given:[3,4,7,8,10,12,13,14],gnu:0,green:9,green_button:9,ground:13,halt:[3,4,14],handl:[11,12],happen:[8,13],hardwar:13,has:[4,10,11,12,13],hasn:[2,13,14],have:[0,10,14],height:12,help:[4,14],helsinki:0,here:[9,10,12,13,14],high:[0,3,11],highest:13,histori:[12,14],history_down:12,history_up:12,hope:0,how:[9,10,12],howev:[3,13,14],http:0,human:4,hv_off:[3,11],hv_off_command:[3,11],hv_on:[3,11],hv_on_command:[3,11],hv_on_statu:[3,11],hvctl:[2,3,4,5,6,7,8,9,10,11,12,14],hvon:14,ident:12,ignor:[4,11],impli:0,imposs:14,includ:[1,3,4,5,8,12,14],incompat:14,increas:12,indent:4,index:[4,12],indic:8,inform:[0,2,3],inhibit:[3,4,7,11],initi:[2,3,4,9,10,11,12],input:[2,4,8,10,11,12],input_:[10,11],inputfil:[2,4,12],insid:[13,14],instal:[0,2],instanc:[3,4,10,14],instanti:7,instead:[2,4,9,10,12,13,14],instruct:13,int_max:[5,7],integ:[5,11,13],intend:[0,1],interact:0,interfac:[1,2,4,8,12,14],interlock:[3,11],interpret:[9,10,14],interv:14,intial:8,intro:4,invalid:4,invis:12,is_answ:7,is_run:10,isn:[4,5,14],issu:2,iter:[2,4,9,12],its:[2,4,7,8,10,12,13,14],itself:13,just:13,keep:[12,13,14],kei:[3,12,13],keypress:12,keyword:5,last:[11,14],lastnam:0,later:[0,5,12],latest:12,launch:14,least:13,left:[2,7,12,13],lemo:13,lenger:3,length:12,less:8,letter:13,librari:[1,12],like:[0,2,4,6,8,10,12,13],line:[2,4,12,14],linearli:13,linux:[0,1,12],list:[0,4,6,12,14],listen:12,load:5,local:[3,4,11,14],locat:[1,2,5,12,13,14],lock:13,longer:4,loop:[2,4],lost:3,lsb:13,machin:10,made:[1,12],mai:[2,4,12,13,14],main:2,mainloop:2,make:[2,4,8,11,12,14],mani:10,manner:[10,11,13],manual:[0,5],match:3,matter:3,max_absolut:12,maximum:[5,12],mean:13,meant:10,member:14,memori:12,merchant:0,messag:[0,3,4,6,11,14],met:11,method:[2,3,4,8,10,11,14],might:0,mode:[0,3,4,7,11],model:13,modifi:[0,12],modul:[0,2,3,4,5,7,8,9,10,11,12,14],more:[0,3,11,13,14],most:[6,10,13],mous:[12,14],mouse_ev:12,move:12,move_cursor_to_end:12,msb:13,multipl:12,multipli:7,must:[1,13],name:[3,4,5,10,11,14],namespac:[6,14],need:[3,4,6,13],neg:[3,12,13],nest:9,never:[5,8],newer:12,newest:12,newlin:8,next:14,non:3,none:[3,4,5,7,8,10,12],normal:[3,4,13],note:13,noth:[8,12],number:[8,11,12,13],numer:13,object:[2,3,4,5,7,8,9,10,11,12,14],off:[3,4,7,11,14],old:[11,12],older:12,oldest:12,onc:10,one:[8,12,13,14],ones:12,onli:[0,4,7,10,12,14],open:[3,11,13,14],open_interlock:11,openpti:8,oper:[0,1,4,13],option:[0,5,14],order:[1,4,11],org:0,origin:12,other:[1,10,12,13,14],otherwis:[3,4,10,11,12,13],output:[2,4,8,10,12],outputfil:[2,4,12],over:11,overrid:14,own:14,packag:[1,6,14],page:[6,14],pair:13,palett:[2,9],panel:[11,13],parallel:[2,3,4,10,14],paramet:[2,3,4,5,9,10,11,12,13],pariti:[5,13],pars:[4,5,11],part:[8,12,14],particular:[0,5],pass:[2,4,11,12],path:[1,5,14],pattern:4,pekko:0,perform:3,physic:[11,13,14],pin:13,plain:4,point:12,polar:[3,13],poll:[3,4,14],port:[3,4,5,10,14],portion:12,posit:12,possibl:[8,10,11,14],potenti:13,power:[13,14],present:[2,9,14],press:[12,13,14],prevent:[2,3,4,7,13],previou:[12,13],previous:12,print:[2,4,8,12,14],probabl:[1,2],problem:13,process:[10,11],produc:[3,5,13],program:[0,2,4,8],programmat:14,prompt:4,properli:14,properti:[7,10,12],protocol:[0,5],provid:[0,4,12,14],pts:10,pty:8,publish:0,pump:13,purpos:0,pyseri:1,python:[0,1,6,10,11,13,14],pythonpath:1,queue:8,queuefil:[0,6],rais:[3,4,5,7,8],rang:[7,11,13],rate:13,read:[2,7,8,10,12,14],readabl:4,readi:0,readlin:[4,8,14],real:14,rear:13,reassign:10,receiv:[0,3,4,7,11,13],recogn:[7,13],red:9,red_button:9,redirect:8,redistribut:0,refer:10,refresh_watchdog:11,regardless:3,register_palett:2,regul:[3,11,14],regular:14,rel:[1,12,14],reload:5,remot:[3,4,11,14],remov:[10,13],render:12,replac:11,repli:3,report:3,repres:7,represent:13,request:4,requir:14,reset:[11,12,13],reset_fault:11,resist:13,resourc:4,respect:11,respond:13,respons:[7,14],restructuredtext:4,result:14,right:13,routin:3,row:12,rtsct:5,run:[1,2,3,4,10,14],running_inst:10,runtimeerror:[3,5],safe:8,safeguard:2,safeti:13,same:[0,3,5,8,12],save:[8,12],scale:13,screen:[2,9,12,14],script:[1,2,14],scroll:[12,14],scrollabl:12,scrollablecommandlin:[2,12],scrollbar:12,scrollbutton:12,scroller:12,scroller_char:12,second:[3,10,11,13,14],section:13,see:[0,1,3,4,5,11,12,14],seem:[0,10],select:12,self:[3,4,7,10,11],send:[2,3,4,7,10,13,14],sent:[3,7,10,11,13,14],sep:4,separ:13,sequenc:13,seri:0,serial:[3,5,7,10,11,14],serial_kwarg:[3,5],serialexcept:3,serv:13,session:14,set:[3,4,5,7,8,10,11,12,14],set_curr:[3,11],set_inhibit:[3,11],set_mod:[3,11],set_text:2,set_voltag:[3,11,14],setcurr:4,seti:4,setu:4,setvoltag:[4,14],sever:[4,5],share:12,shell:14,should:[0,1,2,3,4,5,7,8,10,12],show:14,sign:3,signal:13,signatur:[3,10],signifi:13,signific:13,similar:[0,9,14],simpl:[4,14],simpli:[1,10],simul:[10,11,14],sinc:[0,3,6,11,13],singl:[12,13],size:[8,10,12],skip:3,sleep_tim:10,smallest:5,softwar:0,some:[1,10,13],space:4,specif:[0,13],specifi:[2,4],split:4,sr100kv:[0,3,13],standard:[1,8],start:[4,10,13,14],state:[2,3,11,13],statu:[3,4,7,9,11,14],status_format:[0,6],status_screen:9,status_str:9,statusdict:9,stdin:4,stdout:4,step:[4,11,12],stop:[3,8,10,13],stopbit:5,store:[3,12],str:[3,12],string:[4,7,8,9,12,13],stringio:8,style:2,subminiatur:13,suitabl:10,suppli:[10,14],sure:2,symbol:12,syntax:4,sys:4,system:[0,1],team:0,technix:3,tell:[12,13],temp_histori:12,term:0,termin:[2,12,14],test:[1,11],text:[2,4,9,12],textiobas:8,than:[8,11,12,13],thei:[4,6,14],them:[7,10,13],thi:[0,2,3,4,5,6,7,8,9,10,11,12,13,14],thing:13,those:[0,3,8,12],thread:[2,3,4,8,10,14],through:[2,7,10,11,12,13,14],time:[3,4,8,11,14],time_of_last_command:11,timeout:5,timestep:3,top:[12,14],total_row:12,toward:12,traceback:[3,4,10,11],track:12,ttyusb0:14,tupl:4,turn:[3,4,11,14],tweak:1,two:[11,12,13,14],type:[2,3,4,7,8,10,11,12,13,14],type_:[10,11],typeerror:4,typic:12,unalt:4,uncang:10,under:0,univers:0,unless:13,unsign:[5,11,13],until:10,updat:[3,11,12,14],update_command:12,upon:[3,4,10,11],urwid:[1,2,9,12,14],usag:[0,1],use:[0,4],used:[1,2,3,4,5,7,9,10,12,13,14],useful:0,user:[0,1,2,4,6,9,10,12,14],user_end:10,uses:[1,2,4,5,12,14],using:[1,4,8,14],utf:7,valid:[3,7],valu:[3,4,5,7,8,10,11,12,13,14],valueerror:[3,4,7],variabl:[10,14],veri:0,version:[0,1,5,12],vertic:12,vhv:14,view:12,virtual:[10,11],virtual_end:10,virtualconnect:[0,6,11],virtualhv:[0,6,14],visibl:12,visible_row:12,voltag:[0,3,4,5,7,11,14],voltage_limit:5,wait:[2,4,10,13],warranti:0,watchdog:11,welcom:[4,14],well:14,whatev:13,wheel:[12,14],when:[2,4,5,7,10,11,12,13,14],whenev:[3,12,13,14],where:[4,13],whether:[3,7,8,12,13],which:[0,2,3,5,7,9,10,11,12,13,14],whitespac:4,widget:[0,6,9],width:12,window:[1,14],without:[0,1,8,10,11,13],won:1,work:[0,1,4,10,13],would:8,wrap:[2,8],write:[4,8,10],written:[0,1,2,4,8,10,12],www:0,xonxoff:5,yet:0,you:0,your:[0,1],zero:13},titles:["HVCtl","Installation","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">advanced_tui</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">api</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">command_line_ui</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">config</span></code>","Modules","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">message</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">queuefile</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">status_format</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">virtualconnection</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">virtualhv</span></code>","<code class=\"xref py py-mod docutils literal notranslate\"><span class=\"pre\">widgets</span></code>","RS-232 control protocol","Usage"],titleterms:{"import":14,"switch":13,The:1,Using:14,activ:13,advanced_tui:2,answer:13,api:[3,14],author:0,between:13,bit:13,command:13,command_line_ui:4,compat:0,config:5,control:13,current:13,deactiv:13,depend:1,directori:1,document:0,exampl:14,fault:13,gener:[13,14],get:13,hvctl:[0,1],inhibit:13,instal:1,interact:14,interlock:[13,14],licens:0,list:13,local:13,messag:7,mode:[13,14],model:0,modul:6,off:13,other:0,output:13,protocol:13,queuefil:8,regul:13,remot:13,set:13,statu:13,status_format:9,technix:0,test:14,turn:13,usag:14,virtual:14,virtualconnect:10,virtualhv:11,voltag:13,widget:12,without:14}})