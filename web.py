import random
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Response
import io
from flask import Flask, request, render_template
app = Flask(__name__)


page = '''
<html>
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="fontawesome-free-5.15.1/css/all.css">
    <title>Search</title>
  <script src="https://kit.fontawesome.com/afd6aa68df.js" crossorigin="anonymous"></script>
  <style>
    body{
    margin: 0;
    padding: 0;
    background: #140f1d;
  }
  .box{
      position: relative;
      top: 20%;
      left: 50%;
      transform: translate(-50%,-50%);
  }
  .header {
    position:relative;
    text-align:center;
    color:white;
    padding: 10;
  }
  .header2 {
    position:relative;
    text-align:center;
    color:white;
    padding: 10;
  }
  }
  .inner-header {
    height:65vh;
    width:100%;
    margin: 0;
    padding: 0;
  }
  h1 {
    font-family: 'Lato', sans-serif;
    font-weight:300;
    letter-spacing: 2px;
    font-size:48px;
  }
  h2{
    font-family: 'Lato', sans-serif;
    font-weight:10;
    letter-spacing: 2px;
    font-size:30px;
    color: white;

  }
  .input {
      padding: 10px;
      width: 80px;
      height: 80px;
      background: none;
      border: 4px solid #ffd52d;
      border-radius: 50px;
      box-sizing: border-box;
      font-family: Comic Sans MS;
      font-size: 26px;
      color: #ffd52d;
      outline: none;
      transition: .5s;
  }
  .box:hover input{
      width: 1050px;
      background: #272133;
      border-radius: 10px;
  }
  i{
      position: relative;
      top: 50%;
      right: 15px;
      transform: translate(-50%,-50%);
      font-size: 26px;
      color: #ffd52d;
      transition: .2s;
  }
  .box:hover i{
      opacity: 0;
      z-index: -1;
  }
  </style>
</head>
<body>
    <div class="header">
    <h1>Closest Pair Of Points</h1>
    </div>
    <div class="box">
      <h2>Enter Points as List</h2>
        <form name="search" action ="/result">
            <input type="text" class="input" name="fu"
            onmouseout="document.search.txt.value = ''">
        </form>
            <i class="fas fa-search"></i>
    </div>
    <div class="box">
      <h2>Enter Number of Random Points</h2>
        <form name="search" action ="/result1">
            <input type="text" class="input" name="fu"
            onmouseout="document.search.txt.value = ''">
        </form>
            <i class="fas fa-search"></i>
    </div>
</body>
</html>

'''

fin_page = '''
<img src="/plot.png" alt="my plot">
'''


@app.route("/")
def home():
    return page


@app.route("/result")
def result():
    ind = request.args.get('fu')
    # print(type(ind))
    string = ind
    final = ""
    flag = 0
    ret = []
    for i in string:
        if i == '[' and flag == 0:
            flag = 1
        elif i == ']' and flag == 1:
            s = final.split(',')
            ret.append(s)
            flag = 0
            final = ""
        elif i == ',' and flag == 0:
            continue
        else:
            final = final + i

    for i in range(len(ret)):
        for j in range(2):
            ret[i][j] = int(ret[i][j])

    print(ret)
    sol = cpp(ret)
    sol1 = str(sol[0])
    sol2 = str(sol[1])
    print(sol)
    retval = "The minimum distance is " + sol1 + "\n"+"The closest points are " + sol2
    fig = create_figure(sol, ret)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route("/result1")
def result1():
    ind = request.args.get('fu')
    ret = [[random.randint(0, 1250000), random.randint(0, 1250000)] for i in range(int(ind))]
    print(ret)
    sol = cpp(ret)
    sol1 = str(sol[0])
    sol2 = str(sol[1])
    print(sol)
    retval = "The minimum distance is " + sol1 + "\n"+"The closest points are " + sol2
    fig = create_figure(sol, ret)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure(sol, ret):
    fig = Figure()
    ox = [x[0] for x in ret]
    oy = [x[1] for x in ret]

    axis = fig.add_subplot(1, 1, 1)
    axis.plot(ox, oy, "ro")

    ox = [x[0] for x in sol[1]]
    oy = [x[1] for x in sol[1]]

    axis.plot(ox, oy, "bo-")
    return fig


def cpp(val):
    # Uncomment this for a basic idea of this  BASIC-2 Algorithm
    #P = [[1, 1], [1, 3], [4, 4], [5, 4], [3, 3], [6, 7], [8, 9], [9, 11], [15, 3], [15, 6], [13, 12], [10, 10], [11, 6]]
    P = val

    def Initial_Sort(P):
        Px = sorted(P, key=lambda x: x[0])
        Py = sorted(P, key=lambda x: x[1])
        return Px, Py

    Px, Py = Initial_Sort(P)

    def Euclidean_Distance(P1, P2):
        return math.sqrt((P1[0] - P2[0])**2 + (P1[1] - P2[1])**2)

    def Closest_Pair(Px, Py):
        if len(Px) <= 3:
            Array = Px
            size = len(Array)
            minimum_distance = Euclidean_Distance(Array[0], Array[1])
            Target_Pair = [Array[0], Array[1]]
            if len(Array) == 2:
                return Euclidean_Distance(Array[0], Array[1]), [Array[0], Array[1]]
            for i in range(0, size):
                for j in range(i+1, size):
                    distance = Euclidean_Distance(Array[i], Array[j])
                    if distance < minimum_distance:
                        minimum_distance = distance
                        Target_Pair = [Array[i], Array[j]]

            return minimum_distance, Target_Pair

        midpoint_x = len(Px) // 2
        Qx = Px[:midpoint_x]
        Rx = Px[midpoint_x:]
        median_x = Px[midpoint_x]
        Qy, Ry = [], []

        for point in Py:
            if point[0] < int(median_x[0]):
                Qy.append(point)
            else:
                Ry.append(point)

        min_distance_Left = Closest_Pair(Qx, Qy)
        min_distance_Right = Closest_Pair(Rx, Ry)
        min_distance = min(min_distance_Left, min_distance_Right)
        Target_Pair = min_distance[1]
        Yl, Yr = [], []
        x_bar = Qx[-1][0]

        ll = x_bar - min_distance[0]
        lr = x_bar + min_distance[0]
        for point in Qy:
            if point[0] >= ll:
                Yl.append(point)

        for point in Ry:
            if point[0] <= lr:
                Yr.append(point)
        Yl_sort = sorted(Yl, key=lambda x: x[1])
        Yr_sort = sorted(Yr, key=lambda x: x[1])
        d_min = min_distance[0]
        if (len(Yl_sort) < 1) or (len(Yr_sort) < 1):
            return d_min, Target_Pair
        left = Yl_sort[0]
        right = Yr_sort[0]

        i, j = 0, 0

        while i+1 < len(Yl_sort) and j+1 < len(Yr_sort):
            dist = Euclidean_Distance(left, right)
            if dist < d_min:
                Target_Pair = [left, right]
                d_min = dist
            if left[1] <= right[1]:
                if j < len(Yr_sort):
                    dist = Euclidean_Distance(left, Yr_sort[j+1])
                    if dist < d_min:
                        Target_Pair = [left, Yr_sort[j+1]]
                        d_min = dist

                    left = Yl_sort[i+1]
                    i += 1
            elif i < len(Yl_sort):
                dist = Euclidean_Distance(Yl_sort[i+1], right)
                if dist < d_min:
                    Target_Pair = [Yl_sort[i+1], right]
                    d_min = dist
                right = Yr_sort[j+1]
                j += 1
        return d_min, Target_Pair

    soln = Closest_Pair(Px, Py)
    print("The points are :", P)
    print("\n\n\nThe minimum Distance is : ", soln[0])
    print("\n\nThe Closest Pairs are : ", soln[1])
    return soln


if __name__ == '__main__':
    app.run(debug=True)
