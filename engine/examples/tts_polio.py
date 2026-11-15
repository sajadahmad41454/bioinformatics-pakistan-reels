import soundfile as sf, json, os
from kokoro_onnx import Kokoro
M=os.environ.get("KOKORO_DIR","./")
k=Kokoro(M+"kokoro-v1.0.onnx",M+"voices-v1.0.bin")
lines=[
"Polio is a highly infectious disease caused by a virus, the poliovirus.",
"It spreads mainly through the faecal-oral route, and less often through contaminated water or food.",
"The virus multiplies in the intestine. Most infected people never show symptoms.",
"But if it invades the nervous system, it attacks motor neurons, and can cause paralysis within hours.",
"About one in two hundred infections leads to irreversible paralysis, usually in the legs.",
"Children under five are most at risk.",
"There is no cure for polio. It can only be prevented.",
"Given multiple times, polio vaccines can protect a child for life.",
"Wild poliovirus types two and three have been eradicated.",
"Type one remains endemic in only two countries: Pakistan and Afghanistan.",
"Bioinformatics helps here. Scientists test sewage for poliovirus, often before anyone falls sick.",
"They sequence the viruses they find, and compare them with viruses from patients.",
"Family trees of these sequences reveal transmission links, and genetic gaps can point to missed cases.",
"Vaccinating every child, every time, protects them and helps end polio.",
]
os.makedirs("v_polio",exist_ok=True); durs=[]
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="af_heart",speed=0.99,lang="en-us")
    sf.write(f"v_polio/l{i}.wav",a,sr); durs.append(round(len(a)/sr,2))
json.dump({"v_polio":{"lines":lines,"durs":durs,"sr":sr}},open("tts.json","w"),indent=1)
print(durs,round(sum(durs),1), round(sum(durs)+0.28*13+0.4+2.6,1))
