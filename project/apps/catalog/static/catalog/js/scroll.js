document.addEventListener("DOMContentLoaded", () =>{
    function scrollRight(self){
        const parent = self.parentElement
        const scroll = parent.querySelectorAll('.products-list')
        
        
        scroll.forEach(i => {
        
        });
    };


    function scrollleft(self){
    };

    window.scrollR = scrollRight; 
    window.scrollL = scrollleft;

});
