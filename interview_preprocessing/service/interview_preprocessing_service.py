from abc import ABC, abstractmethod


class InterviewPreprocessingService(ABC):
    @abstractmethod
    def saveConcatenatedRawJsonFile(self, readFilePath, saveFilePath):
        pass

    @abstractmethod
    def separateJsonFileByInfo(self, readFilePath, saveFilePath):
        pass

    @abstractmethod
    def flattenFileToList(self, filePath):
        pass

    @abstractmethod
    def samplingData(self, interviewList, nAnswer, mQuestion):
        pass

    @abstractmethod
    def transformDataWithPOSTagging(self, answerList, questionList):
        pass

    @abstractmethod
    def cosineSimilarityBySentenceTransformer(self, answerStringList, questionStringList):
        pass

    @abstractmethod
    def cosineSimilarityByNltk(self, answerStringList, questionStringList):
        pass

    @abstractmethod
    def countWantToData(self, keyword, interviewDataPath):
        pass

    @abstractmethod
    def saveSimilarityResult(self, sentenceTransformerCosineSimilarityList, answerList, realQuestionList, questionList,
                             saveFilePath):
        pass

    @abstractmethod
    def intentLabeling(self, interviewList):
        pass

    @abstractmethod
    def splitIntentLabeledData(self, labeledInterviewList, sampleSize):
        pass

    @abstractmethod
    def samplingAndSaveLabeledData(self,
                                   interviewListIntentIsNone, interviewListIntentIsNotNone, sampleSize, saveFilePath):
        pass

