/*
 *bigbluebutton api functions for iff site (ifface) 
 *need crypto-js
 *it-for-free 2014
 */
var BBBapi = new Object();
    BBBapi.serveraddr = "http://conference.main.vsu.ru";
    BBBapi.serverproxy = "itforfree.net/ajx";
    BBBapi.simplepswd = "B54x2Fgv";
    BBBapi.pref = "http://";
    BBBapi.servsalt = "bicsyenEiddEjceywintUjCosDewerdooj";
    BBBapi.meetingid = "iFF0x";
    BBBapi.apiurlpostfix = "/bigbluebutton/api/"
    BBBapi.init = function(){
        //-----prefix init----
        var suf = "http://";
        if(location.href.match("https")=="https"){
           suf="https://";
        };
        var _hostpref = "";
        if(location.href.match("www")=="www"){
            _hostpref = "www.";
        };
        this.pref = suf + _hostpref;
    };
    BBBapi.getMeetingStatus = function(){
        var _cs = CryptoJS.SHA1("isMeetingRunningmeetingID=" + this.meetingid + this.servsalt);
        var _url = this.pref + "/" + this.serverproxy + this.apiurlpostfix + "isMeetingRunning?meetingID=" + this.meetingid + "&checksum=" + _cs;
        $.ajax({
            url: _url,
            type: "GET",
            timeout: 500,
            dataType: 'xml',
            error: this.errorMeetingStatus,
            success: this.readMeetingStatus,
            });
    };
    BBBapi.readMeetingStatus = function(data, statustxt){
        if(data.match("true") == "true"){
            var _st = $("#_status");
            _st.css("color", "green");
            _st.text("Online :)");
         } else if(data.match("false") == "false"){
            var _st = $("#_status");
            _st.css("color", "red");
            _st.text("Offline.");
         }
    };
    BBBapi.errorMeetingStatus = function(data, statustxt){
        console.log("ERROR bbb-api " + statustxt);
        var _st = $("#_status");
        _st.css("color", "red");
        _st.text("Ошибка связи с сервисом.");
    };
    BBBapi.Join = function(){
        if ($("#nik_label").hasClass("error")) {
            return;
        }
        var _name = $("#id_name_bbb").val();
        var _cs = CryptoJS.SHA1("joinmeetingID="+this.meetingid+"&password="+this.simplepswd+"&fullName="+_name+this.servsalt);
        var jhref = this.serveraddr + this.apiurlpostfix + "join?meetingID="+this.meetingid+"&password="+this.simplepswd+"&fullName="+_name+"&checksum="+_cs;
        $("#_join_form_bbb").attr("action", jhref);
        var _jb = $("#_join_b");
        _jb.attr("formaction", jhref);
        window.location.assign(jhref);
    };
////////////////////////////////////////////////////////////////////////////////////////////
function BBBinit(seradr, srvslt){
    BBBapi.init();
    BBBapi.serveraddr = seradr;
    BBBapi.servsalt = srvslt;
}

function BBBGetStatus(){
    BBBapi.getMeetingStatus();   
}

function BBBJoin() {
    BBBapi.Join();
}