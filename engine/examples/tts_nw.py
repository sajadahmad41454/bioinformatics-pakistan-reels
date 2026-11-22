import soundfile as sf, json, os
from kokoro_onnx import Kokoro
M=os.environ.get("KOKORO_DIR","./")
k=Kokoro(M+"kokoro-v1.0.onnx",M+"voices-v1.0.bin")
lines=[
"How does a computer line up two DNA sequences? One classic answer: the Needleman Wunsch algorithm, from a 1970 paper.",
"It finds the best global alignment: both sequences, from end to end.",
"First, pick a scoring scheme. A match is plus one, a mismatch minus one, and a gap minus one.",
"Write one sequence across the top of a grid, and the other down the side.",
"Fill the first row and column with gap penalties: zero, minus one, minus two, and so on.",
"Every other cell takes the best of three moves.",
"Diagonal means a match or a mismatch. Coming from above or from the left means a gap.",
"G against G: zero plus one is one, which beats minus two. So this cell gets one.",
"Repeat this for every cell, row by row.",
"The bottom right cell holds the best total score. Here, it is one.",
"Now trace back, following the winning moves to the top left corner.",
"Diagonal steps pair two letters. A vertical step puts a gap in the top sequence.",
"The result: three matches, one mismatch, and one gap. Score: one.",
"Filling m times n cells takes time and memory proportional to m times n.",
]
os.makedirs("v_nw",exist_ok=True); durs=[]
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="af_heart",speed=0.95,lang="en-us")
    sf.write(f"v_nw/l{i}.wav",a,sr); durs.append(round(len(a)/sr,2))
disp=[l.replace("Needleman Wunsch","Needleman–Wunsch").replace("Smith Waterman","Smith–Waterman").replace("bottom right","bottom-right").replace("top left","top-left").replace("m times n cells","m × n cells").replace("proportional to m times n","proportional to m × n") for l in lines]
json.dump({"v_nw":{"lines":disp,"durs":durs,"sr":sr}},open("tts.json","w"),indent=1)
print(durs,round(sum(durs),1), round(sum(durs)+0.25*14+0.4+2.6,1))
