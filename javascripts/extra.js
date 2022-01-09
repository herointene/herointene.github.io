let mainbody = document.body

let tagmanager = `
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PPTZT5H"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
`; 

let gtm = document.createElement('div');
gtm.innerHTML = tagmanager;
mainbody.prepend(gtm);


