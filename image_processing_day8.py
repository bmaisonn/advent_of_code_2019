from collections import defaultdict
from copy import deepcopy

class Image:
    def __init__(self, wide, tall):
        self.wide = wide
        self.tall = tall
        self.img_array = [[[None for i in range(self.wide)] for j in range(self.tall)] for k in range(10)]

    @classmethod
    def from_path(cls, wide, tall, image_path):
        img = cls(wide, tall)

        with open(image_path) as fimage:
            pixel_idx = 0
            for c in fimage.read():
                if c == '\n':
                    break
                
                layer = pixel_idx // img.nb_pixels
                line = (pixel_idx - layer*img.nb_pixels) //  img.wide
                column = (pixel_idx - layer*img.nb_pixels - line*img.wide) % img.wide

                if layer >= len(img.img_array):
                    img.img_array.extend([[[None for i in range(img.wide)] for j in range(img.tall)] for k in range(10)])
                img.img_array[layer][line][column] = int(c)

                pixel_idx+=1

        return img

    def __str__(self):
        img_repr = ""
        for layer in self.img_array:
            img_repr += '-'*len(layer[0]) + '\n'
            for line in layer:
                img_repr += ' '.join([str(v) for v in line if v is not None]) + '\n'
            img_repr += '-'*len(line) + '\n'
        return img_repr

    @property
    def nb_pixels(self):
        return self.wide*self.tall

def certify(img):
    max_layer_nb_0 = None
    for layer in img.img_array:
        nb_values = defaultdict(int)
        for line in layer:
            for v in line:
                nb_values[v] += 1

        if not max_layer_nb_0 or max_layer_nb_0[0] > nb_values[0]:
            max_layer_nb_0 = nb_values

    print(max_layer_nb_0[1]*max_layer_nb_0[2])

def render(img):
    rendered_img = Image(img.wide, img.tall)

    for i in range(img.wide):
        for j in range(img.tall):
            for k in range(len(img.img_array)):
                pixel_value = img.img_array[k][j][i]
                if pixel_value is None:
                    break
                if pixel_value in (0,1):
                    rendered_img.img_array[0][j][i] = '%' if pixel_value else '.'
                    break

    print(rendered_img)



if __name__ == '__main__':
    img = Image.from_path(25, 6,'img_day7.txt')
    certify(img)
    render(img)

