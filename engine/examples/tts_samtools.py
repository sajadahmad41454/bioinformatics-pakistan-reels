import soundfile as sf, json, os
from kokoro_onnx import Kokoro
M=os.environ.get("KOKORO_DIR","./")
k=Kokoro(M+"kokoro-v1.0.onnx",M+"voices-v1.0.bin")
lines=[
"Your aligner just gave you a SAM file. Now what? Meet SAM tools.",
"SAM tools is a set of utilities for SAM, BAM and CRAM alignment files.",
"A SAM file is plain text: one line per alignment, with eleven required columns.",
"Read name, flag, reference, position, mapping quality, and the CIGAR string.",
"BAM holds the same data, compressed. Our toy file shrank from 5.3 kilobytes to under one.",
"Step one: sort. SAM tools sort orders reads by their leftmost position.",
"Step two: index. SAM tools index creates a B A I file for fast random access.",
"Step three: check. Flag stat counts your reads, based on their flags.",
"In our toy run: 20 reads in total, and 18 mapped. That is 90 percent.",
"Each count has two parts: reads that passed QC, plus reads that failed.",
"Step four: view a region. With the index, it jumps straight to chr1, 200 to 300.",
"Four reads overlap that window. Add minus c to simply count them.",
"Sort, index, check, view. Four commands you will use again and again.",
]
os.makedirs("v_sam",exist_ok=True); durs=[]
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="af_heart",speed=0.95,lang="en-us")
    sf.write(f"v_sam/l{i}.wav",a,sr); durs.append(round(len(a)/sr,2))
disp=[l.replace("SAM tools","SAMtools").replace("Flag stat","flagstat").replace("B A I","BAI").replace("chr1, 200 to 300","chr1:200-300").replace("minus c","-c") for l in lines]
json.dump({"v_sam":{"lines":disp,"durs":durs,"sr":sr}},open("tts.json","w"),indent=1)
print(durs,round(sum(durs),1), round(sum(durs)+0.25*12+0.4+2.6,1))
