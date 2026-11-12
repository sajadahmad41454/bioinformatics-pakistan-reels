import soundfile as sf, json, os
from kokoro_onnx import Kokoro
M=os.environ.get("KOKORO_DIR","./")
k=Kokoro(M+"kokoro-v1.0.onnx",M+"voices-v1.0.bin")
lines=[
"Typhoid fever is caused by a bacterium called Salmonella Typhi.",
"It usually spreads through food or water contaminated with human faeces.",
"Symptoms include prolonged fever, headache, weakness, and abdominal pain.",
"Worldwide, an estimated nine million people get sick with typhoid every year.",
"Some people who recover still carry the bacteria, and can pass them on.",
"Doctors can confirm typhoid by finding the bacteria in a blood sample.",
"In 2016, an extensively drug-resistant, or XDR, strain emerged in Sindh, Pakistan.",
"It resists five classes of antibiotics, including ceftriaxone, a standard treatment.",
"Bioinformatics explained how. Scientists sequenced the genomes of outbreak bacteria.",
"The XDR strain belongs to H58, an already multidrug-resistant lineage.",
"It became XDR in a single step, by picking up a plasmid carrying extra resistance genes.",
"In 2019, Pakistan became the first country to add the typhoid conjugate vaccine to routine immunisation.",
"Safe water, good hygiene, and vaccination all help prevent typhoid.",
]
os.makedirs("v_typhoid",exist_ok=True); durs=[]
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="af_heart",speed=0.98,lang="en-us")
    sf.write(f"v_typhoid/l{i}.wav",a,sr); durs.append(round(len(a)/sr,2))
json.dump({"v_typhoid":{"lines":lines,"durs":durs,"sr":sr}},open("tts.json","w"),indent=1)
print(durs,round(sum(durs),1), round(sum(durs)+0.28*12+0.4+2.6,1))
