from PIL import Image
import numpy as np


class GrayMosaicFilter:
    """ Класс для преобразования изображения в черно-белый pixel art"""

    def __init__(self, image_name, mosaic_size, gradation):
        """ Конструктор класса

            Тест Входных данных
            >>> filter = GrayMosaicFilter('img2.jpg', 10, 5)
            >>> [filter.gradation, filter.mosaic_size]
            [51, 10]

            Тест размера изображения
            >>> image = GrayMosaicFilter('img2.jpg', 10, 5).image_array
            >>> len(image) * len(image[1])
            562500

            Тест градации
            >>> GrayMosaicFilter('img2.jpg', 10, 5).gradation
            51

        :param image_name: Название изображения с его расширением
        :param mosaic_size: Размеры блоков мозайки
        :param gradation: Уровень градации
        """
        self.mosaic_size = mosaic_size
        self.gradation = 255 // gradation
        self.image_array = np.array(Image.open(image_name))

    def apply_filter(self):
        """ Применяет фильтацию к изображению

            Тест размера полученного изображения
            >>> Image.fromarray(GrayMosaicFilter('img2.jpg', 10, 5).apply_filter()).size
            (750, 750)

            :return: Черно-белый пиксель-арт
        """
        height = len(self.image_array)
        width = len(self.image_array[1])
        for x in range(0, width, self.mosaic_size):
            for y in range(0, height, self.mosaic_size):
                brightness_average = self._get_brightness_average(x, y)
                self._set_pixel_color(x, y, brightness_average)
        return self.image_array

    def _get_brightness_average(self, x, y):
        """ Вычисляет среднюю яркость блока мозайки

            Средняя яркость с размером мозайки 10
            >>> GrayMosaicFilter('img2.jpg', 10, 1)._get_brightness_average(1,1)
            18

            Средняя яркость с размером мозайки 1
            >>> GrayMosaicFilter('img2.jpg', 1, 1)._get_brightness_average(1,1)
            19

            Средняя яркость с размером мозайки 100
            >>> GrayMosaicFilter('img2.jpg', 100, 1)._get_brightness_average(1,1)
            36

            :return: Средняя яркость блока мозайки -> int
        """
        return int(
            (self.image_array[x: x + self.mosaic_size, y: y + self.mosaic_size].sum()) / 3 // self.mosaic_size ** 2)

    def _set_pixel_color(self, x, y, average):
        """ Закрашивает блок в переданное значение цвета

            :param x: координата крайнего левого угла блока мозайки
            :param y: координата крайнего левого угла блока мозайки
            :param average: среднее значение цвета блока
        """
        self.image_array[x: x + self.mosaic_size, y: y + self.mosaic_size] = int(average // self.gradation) * \
                                                                             self.gradation


if __name__ == '__main__':
    image_input_name = input("Введите имя исходного изображения:")
    mosaic_size = int(input("Размер мозайки:"))
    gradation_level = int(input("Уровней градации:"))
    image_output_name = input("Название изображения на выходе:")

    filtered_array = GrayMosaicFilter(image_input_name, mosaic_size, gradation_level).apply_filter()
    result_image = Image.fromarray(filtered_array)
    result_image.save(image_output_name)
