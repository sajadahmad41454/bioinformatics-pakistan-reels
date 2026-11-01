import soundfile as sf, json
from kokoro_onnx import Kokoro
M="/tmp/claude-0/-home-claude/68628a1e-6847-57da-97a2-ef1c1d707cfb/scratchpad/tts/"
k=Kokoro(M+"kokoro-v1.0.onnx",M+"voices-v1.0.bin")
lines=[
"Your body contains trillions of cells, and most of them operate under tightly regulated biological controls.",
"So what happens when those controls stop working properly?",
"Cancer can develop when changes in a cell disrupt the systems that regulate growth, division, and survival.",
"Some changes affect genes that normally promote cell growth.",
"Others damage the genes responsible for controlling cell division, or repairing DNA.",
"Over time, certain abnormal cells may gain the ability to multiply uncontrollably, and form a tumor.",
"But cancer is not one single disease. Different cancers develop in different ways.",
"This is where bioinformatics becomes powerful.",
"By analyzing DNA mutations, gene expression patterns, and other molecular data,",
"researchers can investigate what makes a tumor different from healthy tissue.",
"The goal?",
"To understand cancer better, and help scientists identify potential biomarkers and therapeutic targets.",
"Because sometimes, the first step toward a better treatment, is understanding what went wrong inside the cell.",
]
import os; os.makedirs("v_cell",exist_ok=True); durs=[]
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="af_heart",speed=0.93,lang="en-us")
    sf.write(f"v_cell/l{i}.wav",a,sr); durs.append(round(len(a)/sr,2))
json.dump({"v_cell":{"lines":lines,"durs":durs,"sr":sr}},open("tts.json","w"),indent=1)
print(durs,round(sum(durs),1))
