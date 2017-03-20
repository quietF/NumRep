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

    def __init__(self, fileName):

        self.fileName = str(fileName)
        self.image = misc.imread(self.fileName)
        self.cols = len(self.image)
        self.rows = len(self.image[0])

    def get_xcorrelation(self, line_number):
        '''
        :param line_number: int from 1 to rows
        :return: cross correlation between line #line_number and line #line_number-1
        '''

        base_line = np.fft.fft(self.image[line_number])
        base_line[:] = (base_line[:]-np.average(base_line))/(np.std(base_line))
        compared_line = np.fft.fft(np.roll(self.image, 1, axis=0)[line_number])
        compared_line[:] = (compared_line[:] - np.average(compared_line)) / (np.std(compared_line))
        xcorrelation = np.fft.ifft(np.multiply(base_line, np.conjugate(compared_line)))

        return xcorrelation.real


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

        self.xcorrelation_diff = np.zeros(aux_image.cols)
        shifted_lines = 0

        for i in range(1, aux_image.cols):

            xcorrelation = self.get_xcorrelation(i)
            autoxcorrelation = self.get_self_cross_correlation(i)
            xc_argmax = int(np.argmax(xcorrelation))
            self.xcorrelation_max[i] = xcorrelation[xc_argmax]
            self.autoxcorrelation_max[i] = np.max(autoxcorrelation)

            self.xcorrelation_diff[i] = np.abs(self.xcorrelation_max[i] - self.autoxcorrelation_max[i])

            if xc_argmax == 0:
                self.zero_xcorrelation_max[i] = xcorrelation[xc_argmax]

            if (xc_argmax != 0):
                shifted_lines+=1
                #aux_image.image[i] = np.roll(aux_image.image[i], -xc_argmax)

        print(shifted_lines)

        #self.xcorrelation_diff /= np.max(self.xcorrelation_diff)
        self.avg_xcorrelation_maxs_difference = np.average(self.xcorrelation_diff)


        x = np.arange(aux_image.cols)
        plt.plot(x, self.xcorrelation_diff, 'r', x, np.full((aux_image.cols), self.avg_xcorrelation_maxs_difference), 'b')
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

    def shift(self):

        xcorrelation_max = np.zeros(self.cols)
        shift = np.zeros(self.cols, dtype=int)

        for i in range(1, self.cols):

            xcorrelation = self.get_xcorrelation(i)
            shift[i] = (int)(np.argmax(xcorrelation))
            xcorrelation_max[i] = xcorrelation[shift[i]]

            #if (shift[i]!=shift[i-1]) & (xcorrelation_max[i]<0.995) & (xcorrelation_max[i]>0.8): # perfect for desync4.pgm
            if (shift[i] != shift[i - 1]) & (xcorrelation_max[i] < 0.995) & (xcorrelation_max[i] > 0.9):
                self.image[i] = np.roll(self.image[i], -shift[i])

        x=np.arange(self.cols)
        plt.plot(x, xcorrelation_max*np.max(shift), 'b', x, shift, 'r')
        plt.show()

    def shift_image(self, threshold_percentage):

        image_out = Image(self.fileName)
        self.get_threshold()
        shifted_lines = 0

        for i1 in range(1, self.cols):

            xcorrelation = self.get_xcorrelation(i1)
            xcorrelation_self = self.get_self_cross_correlation(i1)
            maxs_xcorrelation_diff = np.abs(np.max(xcorrelation)-np.max(xcorrelation_self))
            xcorrelation_shift = (int)(np.argmax(xcorrelation))
            if (xcorrelation_shift != 0) & (maxs_xcorrelation_diff > threshold_percentage*self.avg_xcorrelation_maxs_difference):
                self.image[i1] = np.roll(self.image[i1], xcorrelation_shift)
                shifted_lines += 1

        print(shifted_lines)

    def clean_up(self, pixels):

        cleaned_lines = 0

        for i1 in range(1, self.cols):

            cross_correlation_argmax = np.argmax(self.get_xcorrelation(i1)).astype(int)

            if cross_correlation_argmax != 0:
                # image_out[i1] = np.roll(image_in, -1, axis=0)[i1]
                self.image[i1][:pixels] = np.roll(self.image, -1, axis=0)[i1][:pixels]
                self.image[i1][self.rows - pixels:] = np.roll(self.image, -1, axis=0)[i1][self.rows - pixels]
                cleaned_lines += 1

        print(cleaned_lines)

    def show_image(self):

        plt.imshow(self.image, cmap=plt.cm.gray)
        plt.show()
