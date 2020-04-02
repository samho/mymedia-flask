(function ($) {
  // Use Strict
  "use strict";
  try {
    $("button#new_user").click(function(){
      $(location).attr('href', '/demo');
    });
  } catch (err) {
    console.log(err);
  }
})(jQuery);