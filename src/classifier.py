def classify_title(input_title):
    from transformers import pipeline
    classifier = pipeline("zero-shot-classification")
    print('classifying title')
    sequence = input_title
    candidate_labels = ["General", "Social Services", "Education", "Health", "Employment", "Safety",
    "Quality of life", "Transportation", "Infrastructure", "Parks",
    "Commercial Development", "Land Use", "Budget"]

    return classifier(sequence, candidate_labels)


def geoparse(text_input):
    from mordecai import Geoparser
    geo = Geoparser()
    return geo.geoparse(text_input)


if __name__ == "__main__":
    test_string = "Traffic & Transportation November Committee Meeting"
    # Call in da
    #class_name = classify_title(test_string)
   # print(class_name)