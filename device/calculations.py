# Program Name: calculations.py
# Date: Mar 09, 2020

class Calculations:

    # members
    # constants
    __INVERSION_POINT = 66
    __TOLERANCE_DEVIATION = 0.05    # to be defined
    __MIN_DIMENSIONING_POINTS = 0
    __MAX_DIMENSIONING_POINTS = 175

    # inversion point
    # bolt point which has a step
    def get_inversion_index(self, dimensions_list):
        for i in range(0, len(dimensions_list) - 1):
            if (abs(float(dimensions_list[i]) - float(dimensions_list[i + 1])) > 1.0):
                return i

        return self.__INVERSION_POINT

    # adjust graph curve to be centered
    def normalize_dimensions(self, dimensions_list):
        # get inversion point
        # critical step
        dif = self.__INVERSION_POINT - self.get_inversion_index(dimensions_list)

        if dif == 0:
            return dimensions_list

        temp_list = []
        first_dim = dimensions_list[0]
        last_dim = dimensions_list[-1]

        if dif > 0:
            for i in range(abs(dif)):
                dimensions_list.pop(len(dimensions_list) - 1)
                temp_list.append(first_dim * (0.990 + (i * 0.001)))

            for i in dimensions_list:
                temp_list.append(i)

            return temp_list

        else:
            for i in range(abs(dif)):
                dimensions_list.pop(0)
                dimensions_list.append(last_dim * (0.999 - (i * 0.001)))

            return dimensions_list

    # check dimensions wether are okay or not
    def check_dimensions(self, dimensions_list, max_dim_list, min_dim_list):
        # dimension normalization
        dimensions_list = self.normalize_dimensions(dimensions_list)

        # removes first and last 3 dimensions to be tested
        for i in range(self.__MIN_DIMENSIONING_POINTS, self.__MAX_DIMENSIONING_POINTS):
            if dimensions_list[i] > (max_dim_list[i] + self.__TOLERANCE_DEVIATION) \
                    or dimensions_list[i] < (min_dim_list[i] - self.__TOLERANCE_DEVIATION):
                        return True

        return False
