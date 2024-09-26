import time
import os

from interview_preprocessing.service.interview_preprocessing_service_impl import InterviewPreprocessingServiceImpl
def calculateCosineSimilarityByNltk(nAnswer, mQuestion, filePath, interviewList):
    interviewPreprocessingService = InterviewPreprocessingServiceImpl.getInstance()
    answerList, realQuestionList, questionList = (
        interviewPreprocessingService.samplingData(interviewList, nAnswer, mQuestion, filePath))

    answerStringList, questionStringList = (
        interviewPreprocessingService.transformSampledData(answerList, questionList))

    startTime = time.time()

    nltkCosineSimilarityList = interviewPreprocessingService.cosineSimilarityByNltk(
        answerStringList, questionStringList
    )

    endTime = time.time()
    print(f"nltk 소요 시간: {endTime - startTime}")

    outputFilename = 'output_nltk.txt'
    with open(outputFilename, 'w', encoding='utf-8') as f:
        for idx, cosineSimilarity in enumerate(nltkCosineSimilarityList):
            topFiveIndex = sorted(range(len(cosineSimilarity)),
                                  key=lambda i: cosineSimilarity[i], reverse=True)[:5]
            topFiveValue = [cosineSimilarity[i] for i in topFiveIndex]

            f.write(f"**실제 질문**: {realQuestionList[idx]}\n")
            f.write(f"**답변**: {answerList[idx]}\n")
            f.write("\n")

            for i, index in enumerate(topFiveIndex):
                f.write(f"**질문{i + 1}**: {questionList[index]}\n")
                f.write(f"**유사도**: {topFiveValue[i]}\n")
            f.write("-------------------------------------------------------------------\n")
        print(f"{outputFilename} 생성")

interview = InterviewPreprocessingServiceImpl()

def concatenateRawData(rawFilePath, concatenatedFilePath):
    interview.saveConcatenatedRawJsonFile(rawFilePath, concatenatedFilePath)

def separateData(concatenatedFilePath, separatedFilePath):
    interview.separateJsonFileByInfo(concatenatedFilePath, separatedFilePath)

def getInterviewList(separatedFilePath):
    return interview.flattenFileToList(separatedFilePath)


# 룰 베이스 의도 라벨링
def labelingIntentByRuleBase(separatedFilePath):
    interviewList = getInterviewList(separatedFilePath)
    labeledInterviewList = interview.intentLabeling(interviewList)

    return labeledInterviewList

def saveSampledLabeledInterview(separatedFilePath, labeledFilePath):
    labeledInterviewList = labelingIntentByRuleBase(separatedFilePath)
    interviewListIntentIsNone, interviewListIntentIsNotNone = (
        interview.splitIntentLabeledData(labeledInterviewList, 200))

    interview.samplingAndSaveLabeledData(
            interviewListIntentIsNone, interviewListIntentIsNotNone, 200, labeledFilePath)

def getLLMIntent(inputFile, labeledFilePath):
    interview.getLLMIntent(inputFile, labeledFilePath)

# 규칙 기반 라벨링 vs 정성 평가 라벨링
def compareLabeling(filePath):
    labeledInterviewList = interview.readFile(filePath)
    differentIntentList = interview.compareLabeledIntent(labeledInterviewList)

    return differentIntentList

def countDifferentLabel(filePath):
    intentList = ['협업 능력', '대처 능력', '적응력', '프로젝트 경험', '자기 개발', '기술적 역량']
    differentIntentList = compareLabeling(filePath)
    countDifferentIntentDict = {intent: 0 for intent in intentList}
    for intent in intentList:
        for differentIntent in differentIntentList:
            if intent == differentIntent.get('rule_based_intent'):
                countDifferentIntentDict[intent] += 1

    return countDifferentIntentDict


if __name__ == '__main__':
    rawFilePath = 'assets\\json_data_raw\\'
    concatenatedFilePath = 'assets\\json_data_concatenated\\'
    separatedFilePath = 'assets\\json_data_separated\\'
    labeledFilePath = 'assets\\json_data_intent_labeled\\'
    labeledInputFile = os.path.join(labeledFilePath, 'sample_intent_labeled_1091_qualitative_eval.json')
    compareLabelFilePath = os.path.join(labeledFilePath, 'sample_intent_labeled_1091_qualitative_eval.json')

    # concatenateRawData(rawFilePath, concatenatedFilePath)
    # separateData(concatenatedFilePath, separatedFilePath)
    # labelingIntentByRuleBase(separatedFilePath)
    # saveSampledLabeledInterview(separatedFilePath, labeledFilePath)
    # getLLMIntent(labeledInputFile, labeledFilePath)
    countDifferentIntentDict = countDifferentLabel(compareLabelFilePath)
    print('count of difference Label : ', countDifferentIntentDict)



# # 유사도 계산
# answerList, realQuestionList, questionList = (
#     interview.samplingData(separatedFilePath, nAnswer=50, mQuestion=10000))

# answerStringList, questionStringList = (
#     interview.transformDataWithPOSTagging(answerList, questionList))

# sentenceTransformerCosineSimilarityList = (
#     interviewPreprocessingService.cosineSimilarityBySentenceTransformer(answerStringList, questionStringList))
#
# saveFilePath = 'assets\\question_answer_similarity'
# interviewPreprocessingService.saveSimilarityResult(sentenceTransformerCosineSimilarityList, answerList, realQuestionList, questionList,
#                      saveFilePath)