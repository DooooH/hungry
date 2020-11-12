import numpy as np
from dtaidistance import dtw, dtw_ndim


class Score(object):
    def percentage_score(self, score):  # To be replaced with a better scoring algorithm, if found in the future
        percentage = 100 - (score * 100)
        return int(percentage)

    def dtwdis(self, model_points, input_points, i, j):
        model_points = model_points.reshape(2 * j, )
        input_points = input_points.reshape(2 * i, )
        model_points = model_points / np.linalg.norm(model_points)
        input_points = input_points / np.linalg.norm(input_points)
        return self.percentage_score(dtw.distance(model_points, input_points))


    def dtwdis_new(self, model_points, input_points):
        return self.percentage_score(dtw_ndim.distance(model_points, input_points))


    def normalize(self, input_test):
        for k in range(0, 17):
            input_test[:, k] = input_test[:, k] / np.linalg.norm(input_test[:, k])
        return input_test


    def compare_separate(self, new_video_coordinates, reference_coordinates, i, j, weights):
        # new_video_coordinates = self.normalize(new_video_coordinates)
        scores = []
        for k in range(0, 17):
            scores.append(self.dtwdis(new_video_coordinates[:, k], reference_coordinates[:, k], i, j))
        return self.apply_weights(weights, scores), scores

    def compare_34dim(self, new_video_coordinates, reference_coordinates, i, j, weights):
        # new_video_coordinates = self.normalize(new_video_coordinates)
        scores = []
        for k in range(0, 17):
            scores.append(self.dtwdis(new_video_coordinates[:, k], reference_coordinates[:, k], i, j))
        return self.apply_weights(weights, scores), scores

    def apply_weights(self, weights, scores):
        return list(map(lambda z: z[0] * z[1], zip(np.array(weights), scores)))
