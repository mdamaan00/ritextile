let mql = window.matchMedia('(max-width: 575px)');
var cw;
if (mql.matches==true){
  cw = 250
}else{
  cw = 290
}

function updateSliderArrowsStatus(
    cardsContainer,
    containerWidth,
    cardCount,
    cardWidth
  ) {
    if (
      $(cardsContainer).scrollLeft() + containerWidth <
      cardCount * cardWidth + 15
    ) {
      $("#slide-right-container").removeClass("disable");
    } else {
      $("#slide-right-container").addClass("disable");
    }
    if ($(cardsContainer).scrollLeft() > 0) {
      $("#slide-left-container").removeClass("disable");
    } else {
      $("#slide-left-container").addClass("disable");
    }
  }
  $(function() {
    // Scroll products' slider left/right
    let div = $("#cards-container");
    let cardCount = $(div)
      .find(".cards")
      .children(".this-card").length;
    let speed = 300;
    let containerWidth = $(".container").width();
    let cardWidth = cw;
  
    updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
  
    //Remove scrollbars
    $("#slide-right-container").click(function(e) {
      if ($(div).scrollLeft() + containerWidth < cardCount * cardWidth) {
        $(div).animate(
          {
            scrollLeft: "+=" + cardWidth
          },
          {
            duration: speed,
            complete: function() {
              setTimeout(
                updateSliderArrowsStatus(
                  div,
                  containerWidth,
                  cardCount,
                  cardWidth
                ),
                1005
              );
            }
          }
        );
      }
      updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
    });
    $("#slide-left-container").click(function(e) {
      if ($(div).scrollLeft() + containerWidth > containerWidth) {
      
        $(div).animate(
          {
            scrollLeft: "-=" + cardWidth
          },
          {
            duration: speed,
            complete: function() {
              setTimeout(
                updateSliderArrowsStatus(
                  div,
                  containerWidth,
                  cardCount,
                  cardWidth
                ),
                1005
              );
            }
          }
        );
      }
      updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
    });
  
    // If resize action ocurred then update the container width value
    $(window).resize(function() {
      try {
        containerWidth = $("#cards-container").width();
        updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
      } catch (error) {
        console.log(
          `Error occured while trying to get updated slider container width: 
              ${error}`
        );
      }
    });
  });
  
  function updateSliderArrowsStatus(
    cardsContainer,
    containerWidth,
    cardCount,
    cardWidth
  ) {
    if (
      $(cardsContainer).scrollLeft() + containerWidth <
      cardCount * cardWidth + 15
    ) {
      $("#slide-right-container-1").removeClass("disable");
    } else {
      $("#slide-right-container-1").addClass("disable");
    }
    if ($(cardsContainer).scrollLeft() > 0) {
      $("#slide-left-container-1").removeClass("disable");
    } else {
      $("#slide-left-container-1").addClass("disable");
    }
  }
  $(function() {
    // Scroll products' slider left/right
    let div = $("#cards-container-1");
    let cardCount = $(div)
      .find(".cards")
      .children(".this-card").length;
    let speed = 300;
    let containerWidth = $(".container").width();
    let cardWidth = cw;
  
    updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
  
    //Remove scrollbars
    $("#slide-right-container-1").click(function(e) {
      if ($(div).scrollLeft() + containerWidth < cardCount * cardWidth) {
        $(div).animate(
          {
            scrollLeft: "+=" + cardWidth
          },
          {
            duration: speed,
            complete: function() {
              setTimeout(
                updateSliderArrowsStatus(
                  div,
                  containerWidth,
                  cardCount,
                  cardWidth
                ),
                1005
              );
            }
          }
        );
      }
      updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
    });
    $("#slide-left-container-1").click(function(e) {
      if ($(div).scrollLeft() + containerWidth > containerWidth) {
        $(div).animate(
          {
            scrollLeft: "-=" + cardWidth
          },
          {
            duration: speed,
            complete: function() {
              setTimeout(
                updateSliderArrowsStatus(
                  div,
                  containerWidth,
                  cardCount,
                  cardWidth
                ),
                1005
              );
            }
          }
        );
      }
      updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
    });
  
    // If resize action ocurred then update the container width value
    $(window).resize(function() {
      try {
        containerWidth = $("#cards-container-1").width();
        updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
      } catch (error) {
        console.log(
          `Error occured while trying to get updated slider container width: 
              ${error}`
        );
      }
    });
  });
  
  function updateSliderArrowsStatus(
    cardsContainer,
    containerWidth,
    cardCount,
    cardWidth
  ) {
    if (
      $(cardsContainer).scrollLeft() + containerWidth <
      cardCount * cardWidth + 15
    ) {
      $("#slide-right-container-2").removeClass("disable");
    } else {
      $("#slide-right-container-2").addClass("disable");
    }
    if ($(cardsContainer).scrollLeft() > 0) {
      $("#slide-left-container-2").removeClass("disable");
    } else {
      $("#slide-left-container-2").addClass("disable");
    }
  }
  $(function() {
    let div = $("#cards-container-2");
    let cardCount = $(div)
      .find(".cards")
      .children(".this-card").length;
    let speed = 300;
    let containerWidth = $(".container").width();
    let cardWidth = cw;
    updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
    $("#slide-right-container-2").click(function(e) {
      if ($(div).scrollLeft() + containerWidth < cardCount * cardWidth) {
        $(div).animate(
          {
            scrollLeft: "+=" + cardWidth
          },
          {
            duration: speed,
            complete: function() {
              setTimeout(
                updateSliderArrowsStatus(
                  div,
                  containerWidth,
                  cardCount,
                  cardWidth
                ),
                1005
              );
            }
          }
        );
      }
      updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
    });
    $("#slide-left-container-2").click(function(e) {
      if ($(div).scrollLeft() + containerWidth > containerWidth) {
        $(div).animate(
          {
            scrollLeft: "-=" + cardWidth
          },
          {
            duration: speed,
            complete: function() {
              setTimeout(
                updateSliderArrowsStatus(
                  div,
                  containerWidth,
                  cardCount,
                  cardWidth
                ),
                1005
              );
            }
          }
        );
      }
      updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
    });
    $(window).resize(function() {
      try {
        containerWidth = $("#cards-container-2").width();
        updateSliderArrowsStatus(div, containerWidth, cardCount, cardWidth);
      } catch (error) {
        console.log(
          `Error occured while trying to get updated slider container width: 
              ${error}`
        );
      }
    });
  });