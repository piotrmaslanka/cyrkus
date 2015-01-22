# coding=UTF-8
X = u"""<!DOCTYPE html>
<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
<script type="text/javascript">

var nodes = %s;

function refresh() {
for (var i=0; i<nodes.length; i++)
draw_node(nodes[i]);
setTimeout(refresh, 20000);
}

function mkrow(title, html) {
var k = $('<div class="right"></div>');
k.html(html);
var l = $('<div class="left"></div>');
l.html(title);
var m = $('<div class="row"></div>');
m.append(k);
m.append(l);
return m;
}

function draw_node(nodename) {
    $.post('/'+nodename, {}, function(data) {
        // construct header
        var node = $('#'+nodename);
        node.empty();

        var ssysmon = data['node']['data']['ssysmon'];
        var cores = ssysmon['cores'];

        var la = '<span class="';
        la += ((ssysmon['loadavg'][0] >= cores) ? 'fail' : 'ok');
        la += '">'+ssysmon['loadavg'][0]+'</span> <span class="';
        la += ((ssysmon['loadavg'][1] >= cores) ? 'fail' : 'ok');
        la += '">'+ssysmon['loadavg'][1]+'</span> <span class="';
        la += ((ssysmon['loadavg'][2] >= cores) ? 'fail' : 'ok');
        la += '">'+ssysmon['loadavg'][2]+'</span>';

        var offline = data['secs_ago'] > data['node']['reporting_interval']*3;
        offline = (offline ? 'fail' : 'black');

        var header = $('<div class="header"><div class="header '+offline+'">'+nodename+'</div><div class="ip">'+data['node']['ip']+'</div></div>');
        node.append(header);

        var secsago = '<span class="'+offline+'">'+data['secs_ago']+' sek. temu</span>';

        node.append(mkrow('Ostatni raport', secsago));
        node.append(mkrow('Procesów', ssysmon['running_processes']+'/'+ssysmon['total_processes']));
        node.append(mkrow('Load average', la));

        var memavail = Math.floor(ssysmon['avail_memory'] / 1024);
        var diskavail = Math.floor(ssysmon['free_disk'] / 1024);
        var swapavail = Math.floor(ssysmon['free_swap'] / 1024);

        memavail = '<span class="'+((memavail < 100) ? 'fail' : 'ok')+'">'+memavail+' MB</span>';
        diskavail = '<span class="'+((diskavail < 100) ? 'fail' : 'ok')+'">'+diskavail+' MB</span>';
        swapavail = '<span class="'+((swapavail < 100) ? 'fail' : 'ok')+'">'+swapavail+' MB</span>';

        node.append(mkrow('Całkowity RAM', Math.floor(ssysmon['total_memory']/1024)+' MB'));
        node.append(mkrow('Dostępny RAM', memavail));
        node.append(mkrow('Całkowity HDD', Math.floor(ssysmon['total_disk']/1024)+' MB'));
        node.append(mkrow('Dostępny HDD', diskavail));
        node.append(mkrow('Całkowity SWAP', Math.floor(ssysmon['total_swap']/1024)+' MB'));
        node.append(mkrow('Dostępny SWAP', swapavail));

    });
}

$(refresh);
</script>
<style type="text/css">
#header {
width: 800px;
margin-left: auto;
margin-right: auto;
border-top: 1px solid black;
border-bottom: 1px solid black;
margin-bottom: 10px;
text-align: center;
font-size: 3em;
background-color: lightblue;
}
#content {
width: 800px;
margin-left: auto;
margin-right: auto;
}
.node {
margin-bottom: 10px;
width: 250px;
border: 1px solid black;
float: left;
margin-right: 7px;
margin-left: 7px;
}
.node > .header {
border-bottom: 1px solid black;
background-color: lightblue;
}
.node > .header > .header {
text-align: center;
width: 250px;
font-size: 2em;
}
.node .header .ip {
text-align: center;
width: 250px;
color: gray;
}
.node .row {
width: 250px;
clear: both;
}
.node .row .left {
width: 120px;
padding-left: 5px;
float: left;
}
.node .row .right {
width: 120px;
float: right;
text-align: right;
padding-right: 5px;
}
.ok { color: green; }
.fail { color: red; font-weight: bold; }
</style>
</head><body>
<div id="header">Cyrkus Monitor</div>
<div id="content">%s</div>
</body></html>
"""

def fformat(last_data, last_records):
    """
    @param last_data: dictionary(node_name => node's data segment)
    @param last_records: dictionary(node_name => timestamp, node when
                                                 last transmitted)
    @return: html
    """

    nodelist = last_data.keys()

    a = repr(map(str, nodelist))
    b = ''.join(['<div id="'+x+'" class="node"></div>' for x in nodelist])

    return (X % (a, b)).encode('utf8')
