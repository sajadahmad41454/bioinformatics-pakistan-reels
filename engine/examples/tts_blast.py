import soundfile as sf, json, os
from kokoro_onnx import Kokoro
M=os.environ.get("KOKORO_DIR","./")
k=Kokoro(M+"kokoro-v1.0.onnx",M+"voices-v1.0.bin")
lines=[
"You have a DNA sequence. What is it, and where else does it appear? BLAST helps you find out.",
"The Basic Local Alignment Search Tool finds regions of local similarity between your sequence and a database.",
"Blast N compares DNA with DNA. Blast P, protein with protein.",
"Blast X translates DNA and searches it against proteins.",
"On the command line you need a query in FASTA format, and a database.",
"Make blast D B turns a FASTA file into a database. D B type nucl means DNA.",
"Then run blast N with the query, the database, an output file, and out format 6, for a table.",
"Here is the real result of our toy run. One row per hit.",
"97 percent identity: three mismatches in one hundred bases, no gaps.",
"Query bases 1 to 100 match bases 101 to 200 of gene B.",
"The E-value is the number of hits expected by chance. Lower means more significant.",
"Here it is about ten to the minus 46, so this is very unlikely to be chance.",
"No command line? Paste your sequence into the BLAST web page at NCBI.",
]
os.makedirs("v_blast",exist_ok=True); durs=[]
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="af_heart",speed=0.95,lang="en-us")
    sf.write(f"v_blast/l{i}.wav",a,sr); durs.append(round(len(a)/sr,2))
disp=[l.replace("Blast N","blastn").replace("blast N","blastn").replace("Blast P","blastp").replace("Blast X","blastx").replace("Make blast D B","makeblastdb").replace("D B type","dbtype").replace("out format 6","outfmt 6").replace("ten to the minus 46","10 to the minus 46") for l in lines]
json.dump({"v_blast":{"lines":disp,"durs":durs,"sr":sr}},open("tts.json","w"),indent=1)
print(durs,round(sum(durs),1), round(sum(durs)+0.25*12+0.4+2.6,1))
