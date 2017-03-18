import numpy as np
import matplotlib.pyplot as plt
from scipy import misc


class Image(object):
    '''
    Class to fix a .pgm image with randomly shifted lines.
    :param fileName is the path to a .pgm file
    '''

    image = 0.
    cols = 0
    rows = 0

    avg_xcorrelation_maxs_difference = 0.
    avg_zero_xcorrelation_maxs_difference = 0.
    avg_nonzero_xcorrelation_maxs_difference = 0.

    def __init__(self, fileName):

        self.fileName = str(fileName)
        self.image = misc.imread(self.fileName)
        self.cols = len(self.image)
        self.rows = len(self.image[0])

    def get_cross_correlation(self, line_number):
        '''
        :param image: np.array(rows, cols) of uint8 type
        :param line_number: int from 1 to rows
        :return: cross correlation between line #line_number and line #line_number-1
        '''
        compared_line = np.fft.fft(self.image[line_number])
        base_line = np.fft.fft(np.roll(self.image, 1, axis=0)[line_number])
        cross_correlation = np.fft.ifft(np.multiply(base_line, np.conjugate(compared_line)))

        return cross_correlation.real

    def get_self_cross_correlation(self, line_number):
        '''
        :param image: np.array(rows, cols) of uint8 type
        :param line_number: int from 1 to rows
        :return: self cross correlation of line #line_number
        '''
        line = np.fft.fft(self.image[line_number])
        cross_correlation = np.fft.ifft(np.multiply(line, np.conjugate(line)))

        return cross_correlation.real

    def get_threshold(self):

        aux_image = Image(fileName=self.fileName)
        self.zero_xcorrelation_max = np.zeros(aux_image.cols)
        self.xcorrelation_max = np.zeros(aux_image.cols)
        self.autoxcorrelation_max = np.zeros(aux_image.cols)
        shifted_lines = 0

        for i in range(1, aux_image.cols):

            xcorrelation = self.get_cross_correlation(i)
            autoxcorrelation = self.get_self_cross_correlation(i)
            xc_argmax = int(np.argmax(xcorrelation))
            self.xcorrelation_max[i] = xcorrelation[xc_argmax]
            self.autoxcorrelation_max[i] = np.max(autoxcorrelation)

            if xc_argmax == 0:
                self.zero_xcorrelation_max[i] = xcorrelation[xc_argmax]

            if (xc_argmax != 0):# & (self.xcorrelation_max[i] > self.autoxcorrelation_max[i]):
                shifted_lines+=1
                aux_image.image[i] = np.roll(aux_image.image[i], xc_argmax)

        print(shifted_lines)
        plt.subplot(121), plt.imshow(aux_image.image, cmap=plt.cm.gray)
        plt.subplot(122), plt.imshow(self.image, cmap=plt.cm.gray)
        plt.show()
        plt.close()

        x = np.arange(aux_image.rows)
        plt.plot(x, self.xcorrelation_max, 'r', self.zero_xcorrelation_max, 'b', x, self.autoxcorrelation_max, 'g')
        plt.show()

    """
    def plot_maximums_difference(self):

        self.get_threshold()
        range = np.arange(self.cols)
        averages_cc = np.full((self.cols), self.avg_xcorrelation_maxs_difference)
        nonzero_averages_cc = np.full((self.cols), self.avg_nonzero_xcorrelation_maxs_difference)
        zero_average_cc = np.full((self.cols), self.avg_zero_xcorrelation_maxs_difference)

        plt.plot(range, self.cross_correlation_maxs_diff, 'r', range, averages_cc, 'b--', range, nonzero_averages_cc,
                 'g', range, zero_average_cc, 'y')
        plt.show()
    """

    def shift_image(self, threshold_percentage):

        image_out = Image(self.fileName)
        shifted_lines = 0

        for i1 in range(1, self.cols):

            xcorrelation = self.get_cross_correlation(i1)
            xcorrelation_self = self.get_self_cross_correlation(i1)
            maxs_xcorrelation_diff = np.abs(np.max(xcorrelation)-np.max(xcorrelation_self))
            xcorrelation_shift = (int)(np.argmax(xcorrelation))
            if (xcorrelation_shift != 0) & (
                            self.avg_xcorrelation_maxs_difference * threshold_percentage < maxs_xcorrelation_diff):
                self.image[i1] = np.roll(self.image[i1], xcorrelation_shift)
                shifted_lines += 1

        print(shifted_lines)

    def clean_up(self, pixels):

        cleaned_lines = 0

        for i1 in range(1, self.cols):

            cross_correlation_argmax = np.argmax(self.get_cross_correlation(i1)).astype(int)

            if cross_correlation_argmax != 0:
                # image_out[i1] = np.roll(image_in, -1, axis=0)[i1]
                self.image[i1][:pixels] = np.roll(self.image, -1, axis=0)[i1][:pixels]
                self.image[i1][self.rows - pixels:] = np.roll(self.image, -1, axis=0)[i1][self.rows - pixels]
                cleaned_lines += 1

        print(cleaned_lines)

    def show_image(self):

        plt.imshow(self.image, cmap=plt.cm.gray)
        plt.show()
