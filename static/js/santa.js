function collapse_text() {
    $('#recommendations li p').expander({
        slicePoint:       100,  // default is 100
        expandPrefix:     ' ', // default is '... '
        expandText:       '[...]', // default is 'read more'
        userCollapseText: '',  // default is 'read less'
        expandEffect: 'show',
        expandSpeed: 0
      });
}

page_number = 1;
page_in_progress = false;
santa_current_fbid = 0;
pending_results = '';
stop_update = false;
page_cache = [];
cached_pages = 0;
loop_active = false;

$(document).ready(function(){

    $(document).bind('scroll', onScroll);
    $("#arrow").click(arrow_click);
    $("#friend-picker").focus();

    $("#friend-picker").autocomplete({
        source: friends,
        delay: 200,
        select: function( event, ui ) {
            stop_update = false;
            $('#gifts-topbar').css('display', 'block');
            $('html, body').css('background-color', '#FFFBFB');//f8f1e7
            $("#gifts-topbar h3").html('Gifts for <span class="christmas">' + ui.item.label.split(' ')[0] + "</span>")
            $("#arrow").css('display', 'block');
            $("#ribbon").show();
            $("#friend-picker").hide();
            $("#recommendations").empty().show();
            $("#top-spinner").css('display', 'block');
            $('#splash').css('margin-top', '0px');

            santa_current_fbid = ui.item.id;
            showFriendRequestButton();
  
            page_in_progress = true;
            get_next_page();
        }
    })

    .data("autocomplete")._renderItem = function( ul, item ) {
        return $( "<li>" )
            .data( "item.autocomplete", item )
            .append( "<a><img src='http://graph.facebook.com/" + item.id + "/picture' /><span>" + item.value + "</span></a>" )
            .appendTo( ul );
    };

});

function onScroll(event) {
  //console.log('scrolling');
  var closeToBottom = $(window).scrollTop() + $(window).height() > $(document).height() - 300;

  if(closeToBottom && !page_in_progress) {
    //console.log('close to bottom');
    page_in_progress = true;
    setTimeout(get_next_page, 2000);
  }
};

get_next_page = function() {
  //console.log('get_next');

  if (cached_pages > 0) {
    //console.log('going with an existing page');
    page = pop_page();
    cached_pages--;
    update_recommendations(page);
    page_in_progress = false;
    if (!loop_active) {
      recommend_loop();
    }
  } else {
    //console.log('nothing cached!');
    if (!loop_active) {
      recommend_loop();
    }
    setTimeout(get_next_page, 500);
  }
}

recommend_loop = function() {
  //console.log('recommend loop' + cached_pages);

  loop_active = true;

  if (cached_pages > 2) {
    //console.log('stopping loop');
    loop_active = false;
    return;
  }

  $.ajax({
    type: 'POST', 
    url: '/recommendations',
    data: {
      fbid: santa_current_fbid,
      page: page_number,
      has_liked: has_liked,
    },
    success: function(result) {
      page_cache.push(result);
      cached_pages++;

      page_number = page_number + 1;
      page_in_progress = false;

      recommend_loop(); 
    }
  });
}

pop_page = function() {
  //console.log('pop page');
  return page_cache.pop();
}

update_grid = function(results) {
  $("#recommendations").append(results);
  collapse_text();

  var options = {
    autoResize: true, 
    offset: 15, 
    itemWidth: 315
  };
  
  // Get a reference to your grid items.
  var handler = $('#recommendations li');
  
  // Call the layout function.
  handler.wookmark(options);

  $('#recommendations li').each(function() {
    $(this).click(function() {
      if (has_liked == false) {
        $('#thanks-modal').modal();
      }
    });
  });
  
  // height: 21px;
  //   width: 77px;
}

user_liked_us = function() {
  //console.log("You liked us!");
  has_liked = true;
  update_grid(pending_results);
  pending_results = ''; 
  page_in_progress = false;
  $('li.like-tile').remove();

  var options = {
    autoResize: true, 
    offset: 15, 
    itemWidth: 315
  };

  // Get a reference to your grid items.
  var handler = $('#recommendations li');
  
  // Call the layout function.
  handler.wookmark(options);

  $('#thanks-modal').modal('hide');
}

update_recommendations = function(products) {
  if (stop_update == true) {
    page_number = 1;  
    stop_update = false;
    return;
  }

  $('li.loading-placeholder').remove();

  $("#recommendations").append(products);
  collapse_text();

  var options = {
    autoResize: true, 
    offset: 15, 
    itemWidth: 315
  };
  
  // Get a reference to your grid items.
  var handler = $('#recommendations li');

  // Call the layout function.
    
  handler.imagesLoaded(function() {
    handler.wookmark(options);

    $('li.like-tile.uninitialized').append($('#header-like').html());
    $('li.like-tile.uninitialized').removeClass('uninitialized');
    $('#top-spinner').css('display', 'none');
    $('#spinner').remove();

    $('body').height($('body').height() + 200);

    $('div#footer').removeClass('fixed');
    $('div#footer').css('margin-top', $('body').height()  - 20 + 'px');

    if ($('body').height() < $(window).height() + 300) {
      //console.log('getting next page cause we haven\'t filled the first');
      page_in_progress = true;
      get_next_page();
    }

    $('.ad-container').each(function(){
      if($(this).children().length == 0){
        $(this).append($('#ad-loader').html());
      }
    })

  });
}

arrow_click = function() {
  stop_update = true;
  $("#recommendations").empty().hide();
  $("#content h3").html('Who are you shopping for? <img id="present-tiny" src="/static/images/present-alt2-small.png">');
  $("#arrow").hide();
  $("#ribbon").hide();
  $("#spinner").hide();
  $("#friend-picker").val('').show().focus();
  $('#splash').css('margin-top', '200px');
  $('#gifts-topbar').css('display', 'none');
  $('html, body').css('background-color', 'white');//f8f1e7
  $('div#footer').addClass('fixed');
  $('div#top-spinner').css('display', 'none');
  $('body').height($(window).height());
  page_number = 1;  
  page_cache = [];
  cached_pages = 0;
}
