/*
 *iff video annonce api functions for iff site (ifface) 
 *it-for-free 2014
 */
var iFFapi = new Object();
    iFFapi.serveraddrapi = "itforfree.net/api";
    iFFapi.pref = "http://";
    iFFapi.init = function(){
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
        //----get host name---(might be change in Production manualy):
        this.serveraddrapi = window.location.host + "/api";
    };
    iFFapi.getCookie = function(name){
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    };
    iFFapi.getRequest = function(api, ltimeout, scallback, ercallback){
        var _url = this.pref + "/" + this.serveraddrapi + "/" + api;
        var _timeout = ltimeout || 1500;
        $.ajax({
            url: _url,
            type: "GET",
            timeout: _timeout,
            dataType: "json",
            error: ercallback,
            success: scallback,
            });
    };
    iFFapi.postRequest = function(api, data, ltimeout, scallback, ercallback){
        var _url = this.pref + "/" + this.serveraddrapi + "/" + api;
        var _timeout = ltimeout || 1500;
        var _xsrf = this.getCookie("_xsrf");
        $.ajax({
            url: _url,
            type: "POST",
            data: {"data": JSON.stringify(data), "_xsrf": JSON.stringify(_xsrf)},
            timeout: _timeout,
            dataType: "json",
            error: ercallback,
            success: scallback,
            });
    };
    ////////////////////////////////////////////////////////////////////////////////////
function iFFapiInit() {
    iFFapi.init();
}
function GetVAnonceStatus(){
    var tm = new Object();
    tm.utc = $("#_vutctime").text();
    tm.anutc = $("#_vanutctime").text();
    iFFapi.postRequest("videovnoncestat", tm, 1500, GVASparce, null);
}
function GVASparce(data, status) {
    $("#serv_an_status").text(data.status)
}