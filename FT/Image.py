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
        self.xcorrelation_diff = np.zeros(aux_image.rows)
        self.xcorrelation_diff1= np.zeros(aux_image.rows)
        self.avg_xcorrelation = 0
        self.avg_xcorrelation1 = 0

        for i in range(1, aux_image.cols):

            xcorrelation = aux_image.get_cross_correlation(i)
            xc_argmax = int(np.argmax(xcorrelation))
            xcorrelation_auto = aux_image.get_self_cross_correlation(i)
            self.xcorrelation_diff[i] = np.abs(np.max(xcorrelation)-np.max(xcorrelation_auto))
            self.xcorrelation_diff1[i]= np.abs(np.max(xcorrelation)-xcorrelation_auto[xc_argmax])

            if xc_argmax != 0 :
                aux_image.image[i] = np.roll(aux_image.image[i], -xc_argmax)

        self.avg_xcorrelation = np.average(self.xcorrelation_diff)
        self.avg_xcorrelation1= np.average(self.xcorrelation_diff1)

        print("{0}      {1}".format(self.avg_xcorrelation, self.avg_xcorrelation1))
        aux_image.show_image()


    """
    def get_avg_cross_correlation_max_difference(self):
        '''
        :param image: np.array(rows, cols) of uint8 type
        :return: average absolute value of difference btw:  self cross correlation max AND
                                                            self cross correlation at cross correlation max
        '''

        self.cross_correlation = np.zeros((self.cols, self.rows))
        self.self_cross_correlation = np.zeros((self.cols, self.rows))
        self.cross_correlation_maxs_diff = np.zeros(self.cols)
        nonzero_lines = 0
        zero_lines = 0

        for i1 in range(1, self.cols):
            self.cross_correlation[i1] = self.get_cross_correlation(i1)
            self.self_cross_correlation[i1] = self.get_self_cross_correlation(i1)
            self.cross_correlation_maxs_diff[i1] = np.abs(
                np.max(self.self_cross_correlation[i1]) - np.max(self.cross_correlation[i1]))
            self.avg_xcorrelation_maxs_difference += self.cross_correlation_maxs_diff[i1] / self.cols
            if np.argmax(self.cross_correlation[i1]) != 0:
                nonzero_lines += 1
                self.avg_nonzero_xcorrelation_maxs_difference += self.cross_correlation_maxs_diff[i1]
            else:
                self.avg_zero_xcorrelation_maxs_difference += self.cross_correlation_maxs_diff[i1]
                zero_lines += 1

        print(np.max(self.cross_correlation_maxs_diff))
        print(nonzero_lines)

        self.avg_zero_xcorrelation_maxs_difference /= zero_lines
        self.avg_nonzero_xcorrelation_maxs_difference /= nonzero_lines

    """

    def plot_maximums_difference(self):

        #self.get_avg_max_difference()
        self.get_threshold()

        range = np.arange(self.cols)
        averages_cc = np.full((self.cols), self.avg_xcorrelation_maxs_difference)
        nonzero_averages_cc = np.full((self.cols), self.avg_nonzero_xcorrelation_maxs_difference)
        zero_average_cc = np.full((self.cols), self.avg_zero_xcorrelation_maxs_difference)

        plt.plot(range, self.cross_correlation_maxs_diff, 'r', range, averages_cc, 'b--', range, nonzero_averages_cc,
                 'g', range, zero_average_cc, 'y')
        plt.show()

    def shift_image(self, threshold_percentage):

        # image_out = np.copy(self.image)
        image_out = Image(self.fileName)
        shifted_lines = 0

        #self.plot_maximums_difference()
        self.get_avg_cross_correlation_max_difference()

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
