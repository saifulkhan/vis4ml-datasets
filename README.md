# About


## Define Configuration Files

`distribution.json`

```
{
  /* "valid shapes: circle, square, triangle, <to add>" */
  "shape": ["circle", "square", "triangle"],
  /* nsp_shape: len(shapes), not defined explicitly  */

  /* shape scaling range: min >0, max <= 1, min < max  */
  "scale": [0.2, 0.8],
  "nsp_scale": 8,

  /* position range: min >=0, max <= 1, min < max  */
  "pos_x": [0.2, 0.8],
  "nsp_pos_x": 8,
  "pos_y": [0.2, 0.8],
  "nsp_pos_y": 4,

  /* shape rotation range: min >=0, max <= 360, min < max  */
  "rotation": [0, 180],
  "nsp_rotation": 4,

  /* grey scale range: min >=0, max <= 255, min < max  */
  "grey": [50, 255],
  "nsp_grey": 16

  /* RGB color range: min >=0, max <= 255, min < max  */
  /* to be implemented later, cannot be used with "grey" & "HSV"  */

  /* HSV color range: min >=0, max <= 255, min < max  */
  /* to be implemented later, cannot be used with "grey" & "RGB"  */

  /* more to be added.  */
}
```

`metadata.json`

```
{
  /* number of images: integer > 0  */
  "num_images": 10,

  /* constraint: number of shapes per image: >= 1  */
  "num_shapes": 2

  /* output directory: string directory path  */
  "output_dir": "../output",

  /* output prefix: text string  */
  "output_prefix": "TestData-JC-July24_",

  /* output type: "png", "jpg", <add more later>  */
  /* if jpg is selected, compression is ?  */
  "output_type": "png",

  /* number of output digits: >= 0  */
  /* (if < the digits required for the max, no digits control)  */
  "output_digit": 4,

  /* e.g., TestData-JC-July24_0001, TestData-JC-July24_0002, ...  */

  /* image size (number of pixels): min > 0  */
  "image_width": 64,
  "image_height": 64,

  /* image color types: "grey", "RGB", "HSV"  */
  "color_type": "grey",

  /* image background: "black", "white", "#000000" or other <hex code>  */
  "background": "white",

 

  /* constraint: component distance between a valid color and */
  /* background, min >=0, max < 255 (0 means no constraint) */
  "color_background": 10,

  /* constraint: overlapping: yes (allowed) or no */
  "shape_overlapping": false, 

  /* constraint: cropping: yes (allowed) or no */
  "shape_cropping": false
}

```

## Run Image Generator

```python
python main.py
```
 
