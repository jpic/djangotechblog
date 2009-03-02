
$(function(){
    $('div[id^=oi-]').each(function(){

        var name = $(this).attr('id').substr(3);
        $('#oiarea-'+name).mouseover(function(){
           var h = $('#oi-'+name+' .image-overlay').height();
           $('#oi-'+name+' .overlay-outer').animate({
            'top':-h
           }, 300, 'swing');

        });
        $('#oiarea-' + name).mouseout(function(){
           $('#oi-' + name +' .overlay-outer').animate({
                'top':0
           }, 300, 'swing');

        });
    });
});
