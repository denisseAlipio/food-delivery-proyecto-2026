# Extrae el árbol y los coeficientes exactos de models/m5p_final.model a models/m5p_tree.json
# Requiere: pip install python-weka-wrapper3 (y Java). Ejecutar desde la carpeta raíz del repositorio.
import json, weka.core.jvm as jvm
jvm.start(packages=False, max_heap_size="3g")
import jpype
import weka.core.serialization as ser
o=ser.read("models/m5p_final.model")
def g(obj, cls, name):
    f=jpype.JClass(cls).class_.getDeclaredField(name); f.setAccessible(True); return f.get(obj)
B="weka.classifiers.trees.m5.M5Base"
rule=g(o,B,"m_ruleSet").get(0)
top=g(rule,"weka.classifiers.trees.m5.Rule","m_topOfTree")
RN="weka.classifiers.trees.m5.RuleNode"; LM="weka.classifiers.trees.m5.PreConstructedLinearModel"
hdr=g(o,B,"m_removeUseless").getOutputFormat()
names=[str(hdr.attribute(i).name()) for i in range(hdr.numAttributes())]
cls=hdr.classIndex()
print("attrs:",len(names),"class",names[cls])
def walk(n):
    if bool(g(n,RN,"m_isLeaf")):
        m=g(n,RN,"m_nodeModel")
        c=list(g(m,LM,"m_coefficients"))
        return {"lm":int(g(n,RN,"m_leafModelNum")),"b":float(g(m,LM,"m_intercept")),
                "w":{names[i]:float(c[i]) for i in range(len(c)) if i!=cls and c[i]!=0}}
    return {"a":names[int(g(n,RN,"m_splitAtt"))],"v":float(g(n,RN,"m_splitValue")),
            "l":walk(g(n,RN,"m_left")),"r":walk(g(n,RN,"m_right"))}
tree=walk(top)
feats=[n for i,n in enumerate(names) if i!=cls]
json.dump({"features":feats,"tree":tree},open("models/m5p_tree.json","w",encoding="utf-8"))
print(feats)
jvm.stop()
