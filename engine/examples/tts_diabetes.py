import soundfile as sf, json, os
from kokoro_onnx import Kokoro
M=os.environ.get("KOKORO_DIR","./")
k=Kokoro(M+"kokoro-v1.0.onnx",M+"voices-v1.0.bin")
lines=[
"Type 2 diabetes affects how the body uses sugar for energy. More than 95 percent of people with diabetes have this type.",
"In Pakistan, more than 34 million adults were living with diabetes in 2024.",
"When you eat, glucose enters your blood, and the pancreas releases insulin.",
"Insulin acts like a key that lets glucose into cells.",
"In type 2 diabetes, muscle, fat and liver cells respond poorly to insulin.",
"The pancreas may also make too little, so sugar builds up in the blood.",
"Extra weight, too little exercise, and genetics all raise the risk.",
"Signs include thirst, frequent urination, blurred vision and tiredness.",
"But many people have no symptoms for years.",
"Over time, it can damage blood vessels in the heart, eyes, kidneys and nerves.",
"A simple blood glucose test can find it early.",
"A genetic study of 2.5 million people found 611 genome regions linked to type 2 diabetes.",
"Grouped into eight clusters, they point to different biological pathways.",
"Eat healthy, stay active 150 minutes a week, and don't smoke.",
]
os.makedirs("v_diab",exist_ok=True); durs=[]
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="af_heart",speed=1.0,lang="en-us")
    sf.write(f"v_diab/l{i}.wav",a,sr); durs.append(round(len(a)/sr,2))
json.dump({"v_diab":{"lines":lines,"durs":durs,"sr":sr}},open("tts.json","w"),indent=1)
print(durs,round(sum(durs),1), round(sum(durs)+0.25*13+0.4+2.6,1))
