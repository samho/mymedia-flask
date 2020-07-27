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
  try {
    var ctx = document.getElementById("movie-percent");
    if (ctx) {
      ctx.height = 209;
      var data1 = document.getElementById("movie-percent-data1").getAttribute("data1")
      var data2 = document.getElementById("movie-percent-data2").getAttribute("data2")
      //var dataset = [90,10];
      var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          datasets: [
            {
              label: "My First dataset",
              data: [data1, data2],
              backgroundColor: [
                '#00b5e9',
                '#fa4251'
              ],
              hoverBackgroundColor: [
                '#00b5e9',
                '#fa4251'
              ],
              borderWidth: [
                0, 0
              ],
              hoverBorderColor: [
                'transparent',
                'transparent'
              ]
            }
          ],
          labels: [
            'Regular',
            'Adult'
          ]
        },
        options: {
          maintainAspectRatio: false,
          responsive: true,
          cutoutPercentage: 87,
          animation: {
            animateScale: true,
            animateRotate: true
          },
          legend: {
            display: false,
            position: 'bottom',
            labels: {
              fontSize: 14,
              fontFamily: "Poppins,sans-serif"
            }

          },
          tooltips: {
            titleFontFamily: "Poppins",
            xPadding: 15,
            yPadding: 10,
            caretPadding: 0,
            bodyFontSize: 16,
          }
        }
      });
    }
  }catch (err) {
    console.log(err);
  }
})(jQuery);