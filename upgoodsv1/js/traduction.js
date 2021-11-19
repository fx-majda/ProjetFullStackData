function translate_page(lang)
{
	var url = self.location;
    var base = document.getElementsByTagName('base');
    if(base.length>0)
    {
    	url = base[0].href;
    }
	top.location='http://www.google.com/translate?hl=fr&sl=auto&tl='+lang+'&u='+url;
    return true;
}
var html_711 = "<a style=\"cursor:pointer;margin:1px;display:inline-block;\" onclick=\"translate_page(\'en\');\"><div style=\"width:50px;height:25px;background:url(\'http://services.supportduweb.com/translator/styles/images/s1.png\');background-position:-0px 0px;display:inline-block;padding:0px;margin:0px;\" onmouseover=\"this.style.backgroundPosition=\'-0px -25px\';\" onmouseout=\"this.style.backgroundPosition=\'-0px 0px\';\" alt=\"English\"></div></a><a style=\"cursor:pointer;margin:1px;display:inline-block;\" onclick=\"translate_page(\'es\');\"><div style=\"width:50px;height:25px;background:url(\'http://services.supportduweb.com/translator/styles/images/s1.png\');background-position:-50px 0px;display:inline-block;padding:0px;margin:0px;\" onmouseover=\"this.style.backgroundPosition=\'-50px -25px\';\" onmouseout=\"this.style.backgroundPosition=\'-50px 0px\';\" alt=\"Espa&ntilde;ol\"></div></a><a style=\"cursor:pointer;margin:1px;display:inline-block;\" onclick=\"translate_page(\'fr\');\"><div style=\"width:50px;height:25px;background:url(\'http://services.supportduweb.com/translator/styles/images/s1.png\');background-position:-150px 0px;display:inline-block;padding:0px;margin:0px;\" onmouseover=\"this.style.backgroundPosition=\'-150px -25px\';\" onmouseout=\"this.style.backgroundPosition=\'-150px 0px\';\" alt=\"Fran&ccedil;ais\"></div></a>";
document.getElementById('translator_711').innerHTML=html_711;