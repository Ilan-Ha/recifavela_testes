import json
import pandas as pd
from pathlib import Path
import os

pwd = os.path.join("images","datasets","vencerlanz09","bottle-synthetic-images-dataset","versions","7","ImageClassesCombinedWithCOCOAnnotations","coco_instances.json")

def cvv_creator():
    with open(pwd, "r") as f:
        annotations = json.load(f)

    ipath = []
    lbl = []
    bbox = []
    labels = {}
    labels["ids"] = []
    labels["categories"] = []
    for category in annotations["categories"]:
        labels["ids"].append(category["id"])
        labels["categories"].append(category["name"])
    # print(labels)
    # for key, value in annotations.items():
    #     print(f"Key:{key}")
    # for n in range(6):
    #     id = annotations["annotations"][n]["image_id"]
    #     cat = annotations["annotations"][n]["category_id"] - 1
    #     print(f"categoria: {labels["categories"][cat]}| imagem referencia: {id} | nome: {annotations["images"][id]["file_name"]}")

    # print(annotations["images"][0])
    # print(annotations["annotations"][10])
    for annotation in annotations["annotations"]:

        material = annotation["category_id"]
        if material in labels["ids"]:
            label = labels["categories"][material-1]
        else:
            label = "other"
        image_id = annotation["image_id"]
        filename = annotations["images"][image_id]["file_name"]
        box = annotation['bbox']
        ipath.append(os.path.join("images","datasets","vencerlanz09","bottle-synthetic-images-dataset","versions","7","ImageClassesCombinedWithCOCOAnnotations","images_raw",filename))
        lbl.append(label)
        bbox.append(box)

    data = {'path':ipath,'label':lbl,'bbox':bbox}
    df = pd.DataFrame(data)
    df.to_csv('bottle-synthetic-images-dataset.csv',index=False)

    # plastic = df[df["label"]=="plastic"]
    # plastic.to_csv('bottle-synthetic-images-dataset-plastic.csv',index=False)

cvv_creator()