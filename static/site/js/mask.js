"use strict";
{
    function configure(){
        let inputs = document.querySelectorAll('[data-inputmask]');
        inputs = Array.from(inputs).filter(function(input){
            return  !input.hasAttribute("data-money-input");
        });
        inputs.forEach(function(element){
            let opts = element.getAttribute('data-inputmask').replace(/&quot;/g, '"');
            let im = new Inputmask(opts);
            im.mask(element)
        });
    }
    // Call function fn when the DOM is loaded and ready. If it is already
    // loaded, call the function now.
    // http://youmightnotneedjquery.com/#ready
    function ready(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }
    ready(function() {
        configure();
    });
}