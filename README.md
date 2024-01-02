# AI答复机器人 （图数据库查询部分）

## 通过症状查询

```js
MATCH (u:Symptom)-[:has_symptom]-(d:Disease)
WHERE u.name IN ['发烧', '咳嗽', '右上腹痛', '头昏', '呕吐', '斑丘疹']
WITH d, COUNT(*) AS relevance
MATCH (d)-[:belongs_to]-(department:Department)
WITH department,d,relevance
MATCH (department)-[:works_in]-(doc:Doctors)
WITH department,d,relevance,doc
MATCH (department)
WHERE doc.working_hospital ='宁波市中医院'
RETURN doc.name, d.name, department.name,relevance 
ORDER BY relevance DESC LIMIT 10
``````
### 结果
<center>
<table>
<thead>
  <tr>
    <th>doc.name</th>
    <th>d.name</th>
    <th>department.name</th>
    <th>relevance</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>"周晶晶"</td>
    <td>"老年人支原体肺炎"</td>
    <td>"呼吸内科"</td>
    <td>3</td>
  </tr>
  <tr>
    <td>"李鑫"</td>
    <td>"老年人支原体肺炎"</td>
    <td>"呼吸内科"</td>
    <td>3</td>
  </tr>
  <tr>
    <td>"应秋华"</td>
    <td>"小儿埃可及柯萨奇病毒感染"</td>
    <td>"血液内科"</td>
    <td>3</td>
  </tr>
  <tr>
    <td>"潘胜美"</td>
    <td>"小儿埃可及柯萨奇病毒感染"</td>
    <td>"血液内科"</td>
    <td>3</td>
  </tr>
  <tr>
    <td>"楼金杰"</td>
    <td>"小儿埃可及柯萨奇病毒感染"</td>
    <td>"血液内科"</td>
    <td>3</td>
  </tr>
  <tr>
    <td>"郑戴波"</td>
    <td>"小儿埃可及柯萨奇病毒感染"</td>
    <td>"血液内科"</td>
    <td>3</td>
  </tr>
  <tr>
    <td>"李梦瑶"</td>
    <td>"小儿支原体肺炎"</td>
    <td>"中医儿科"</td>
    <td>3</td>
  </tr>
  <tr>
    <td>"沈桂珍"</td>
    <td>"小儿支原体肺炎"</td>
    <td>"中医儿科"</td>
    <td>3</td>
  </tr>
  <tr>
    <td>"王倩"</td>
    <td>"小儿支原体肺炎"</td>
    <td>"中医儿科"</td>
    <td>3</td>
  </tr>
  <tr>
    <td>"丁瑾"</td>
    <td>"小儿支原体肺炎"</td>
    <td>"中医儿科"</td>
    <td>3</td>
  </tr>
</tbody>
</table>
</center>

### 根据症状查找科室

```js
MATCH (u:Symptom)-[:has_symptom]-(d:Disease)
WHERE u.name IN ['发烧', '咳嗽', '右上腹痛', '头昏', '呕吐', '斑丘疹']
WITH d, COUNT(*) AS relevance
MATCH (d)-[:belongs_to]-(department:Department)
RETURN d.name,department.name
ORDER BY relevance DESC LIMIT 10
```
### 结果
<center>
<table>
<thead>
  <tr>
    <th>d.name</th>
    <th>department.name</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>"小儿麻疹"</td>
    <td>"传染科"</td>
  </tr>
  <tr>
    <td>"麻疹"</td>
    <td>"传染科"</td>
  </tr>
  <tr>
    <td>"类圆线虫病"</td>
    <td>"传染科"</td>
  </tr>
  <tr>
    <td>"风疹"</td>
    <td>"传染科"</td>
  </tr>
  <tr>
    <td>"旋毛虫病"</td>
    <td>"传染科"</td>
  </tr>
  <tr>
    <td>"水痘"</td>
    <td>"传染科"</td>
  </tr>
  <tr>
    <td>"老年人支原体肺炎"</td>
    <td>"呼吸内科"</td>
  </tr>
  <tr>
    <td>"猫抓病"</td>
    <td>"传染科"</td>
  </tr>
  <tr>
    <td>"小儿埃可及柯萨奇病毒感染"</td>
    <td>"血液内科"</td>
  </tr>
  <tr>
    <td>"传染性单核细胞增多症"</td>
    <td>"传染科"</td>
  </tr>
</tbody>
</table>
</center>


```js
MATCH (u:Symptom)-[:has_symptom]-(d:Disease)
WHERE u.name IN ['腱鞘炎','手痛'] 
WITH d,COUNT(*) AS relevance
// MATCH (d)-[:has_symptom]-(s:Symptom)
// WITH d, relevance, COUNT(s) AS symcount,size(['发烧', '咳嗽']) AS relevance2
// WITH d, relevance,tofloat(relevance) / tofloat(symcount+relevance2) AS relevance_ratio
MATCH (d)-[:belongs_to]-(department:Department)
RETURN department.name,sum(relevance) as s_rel
ORDER BY s_rel DESC 
```