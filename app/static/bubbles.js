function myFunction(artists) {
  // var xmlhttp = new XMLHttpRequest();
  // var url = "http://sweetify.me/api/artists";
  // var character_counts = []
  // xmlhttp.onreadystatechange = function() {
  //    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
  //        window.alert(xmlhttp.responseText);
  //        var myArr = JSON.parse(xmlhttp.responseText.result);
  //       character_counts = dict()
  //       for author in authors :
  //         c = author.upper()[0]
  //         if c in character_counts :
  //           character_counts[c] += 1
  //         else :
  //           character_counts[c] = 1        
  //         character_counts = [{'text':key,'count':character_counts[key]} for key in character_counts]     
  //         var dict;
  //        for (var i = 0; i < myArr.length; i++)
  //        {

  //        }
  //    }
  // };
  // xmlhttp.open("GET", url, true);
  // xmlhttp.send();
  // var character_counts = {{ character_counts|tojson }}

  var bubbleChart = new d3.svg.BubbleChart({
    supportResponsive: true,
    //container: => use @default
    size: 1250,
    //viewBoxSize: => use @default
    innerRadius: 150,
    //outerRadius: => use @default
    radiusMin: 40,
    radiusMax: 100,
    //intersectDelta: use @default
    //intersectInc: use @default
    //circleColor: use @default
    data: {
         items: artists, 
      // items: [
      //   {text: "Java", count: "236"},
      //   {text: ".Net", count: "382"},
      //   {text: "Php", count: "170"},
      //   {text: "Ruby", count: "123"},
      //   {text: "D", count: "12"},
      //   {text: "Python", count: "170"},
      //   {text: "C/C++", count: "382"},
      //   {text: "Pascal", count: "10"},
      //   {text: "Something", count: "170"},
      //   {text: "Java1", count: "236"},
      //   {text: ".Net1", count: "382"},
      //   {text: "Php1", count: "170"},
      //   {text: "Ruby1", count: "123"},
      //   {text: "D1", count: "12"},
      //   {text: "Python1", count: "170"},
      //   {text: "C/C++1", count: "382"},
      //   {text: "Pascal1", count: "10"},
      //   {text: "Something1", count: "170"},
      // ],
      eval: function (item) {return item.count;},
      classed: function (item) {return item.text.split(" ").join("");}
    },
    plugins: [
      {
        name: "central-click",
        options: {
          text: "(See more detail)",
          style: {
            "font-size": "12px",
            "font-style": "italic",
            "font-family": "Source Sans Pro, sans-serif",
            //"font-weight": "700",
            "text-anchor": "middle",
            "fill": "white"
          },
          attr: {dy: "65px"},
          centralClick: function() {
            alert("Here is more details!!");
          }
        }
      },
      {
        name: "lines",
        options: {
          format: [
            {// Line #0
              textField: "count",
              classed: {count: true},
              style: {
                "font-size": "28px",
                "font-family": "Source Sans Pro, sans-serif",
                "text-anchor": "middle",
                fill: "white"
              },
              attr: {
                dy: "0px",
                x: function (d) {return d.cx;},
                y: function (d) {return d.cy;}
              }
            },
            {// Line #1
              textField: "text",
              classed: {text: true},
              style: {
                "font-size": "14px",
                "font-family": "Source Sans Pro, sans-serif",
                "text-anchor": "middle",
                fill: "white"
              },
              attr: {
                dy: "20px",
                x: function (d) {return d.cx;},
                y: function (d) {return d.cy;}
              }
            }
          ],
          centralFormat: [
            {// Line #0
              style: {"font-size": "50px"},
              attr: {}
            },
            {// Line #1
              style: {"font-size": "30px"},
              attr: {dy: "40px"}
            }
          ]
        }
      }]
  });
}