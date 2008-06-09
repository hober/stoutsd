var Stout = function () {
  var images = ["/images/stout-main.jpg", "/images/guinness-bw.jpg",
                "/images/pub-open.jpg"];
  var duration = 6000;
  var el;
  var current = 0;
  var next = function () {
    el.attr({src: images[current]});
    current = current + 1;
    if (current == images.length) {
      current = 0;
    }
  };
  var advance = function () {
    setTimeout(advance, duration);
    next();
  };
  return {
    ready: function () {
      el = $("#slideshow");
      if (el) {
        advance();
        el.click(next);
      }
    }
  };
}();

$(Stout.ready);
