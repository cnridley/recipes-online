  $(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $('select').formSelect();
    $('#favouriteBtn').click(function(){
        $('#favouriteBtn').css('backgroundColor', '#f44336');
        $('#favouriteBtn').css('color', 'black');
    });
  });

 