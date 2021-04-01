It is best to have text on a grid that accurately scales to the size screen, and more so on a 3:4 rectangle. I wrote this to make sense of the math, google didn't help me.

## Notice that:
1.) If there's a rectangle with a ratio of w/h, and it is divided it into four equal parts, the width over height of each individual rectangle will be the same as it's parent rectangle.

[2.)](https://www.desmos.com/calculator/a4dawbzz4v) Any rectangle can have a 3:4 rectangle cut from it, with both rectangles sharing a side. 

## Process
First create a large 3:4 rectangle.
Multiply the width of the screen by 4/3 to scale it and get a y-value. If this value exceeds the height of the screen, the width cannot form a 3:4 rectangle without exceeding the screen, and the height must be used. To use the height for the rectangle, multiply it by 3/4. Either way, a large 3:4 rectangle has been formed.

Divide this rectangle into fourths, each of those into fourths, and each of those into fourths. In other words, divide the rectangle into sixty four parts, eight by eight. The width and height of the smallest rectangle is unit width and height of the new grid. 

Appened more rects to the sides of the grid space as needed to fill it without exceeding it.