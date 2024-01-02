#!/usr/bin/env python3
# coding: utf-8
# File: MedicalGraph.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-3

import os
import json
from py2neo import Graph, Node


class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        # self.data_path = os.path.join(cur_dir, 'data/medical.json')
        self.data_path = os.path.join(cur_dir, 'data/medical_rebuild.json')  # 键'symptom'的值是从新爬取的，对其了网址的症状库。
        self.g = Graph('bolt://10.1.51.23:7691', auth=("neo4j", "kt123456"))

    '''读取文件'''

    def read_nodes(self):
        # 共７类节点 每类内部节点不重复
        drugs = []  # 药品
        foods = []  # 食物
        checks = []  # 检查
        departments = []  # 科室
        producers = []  # 药品大类
        diseases = []  # 疾病
        symptoms = []  # 症状
        hospitals = []
        doctor_department_relations = []
        department_hospital_relations = []
        disease_infos = []  # 疾病信息
        doctors_and_hospitals=[]
        # 构建节点实体关系
        rels_department = []  # 科室－科室关系 eg ['呼吸内科', '内科'] 小科室-大科室
        rels_noteat = []  # 疾病－忌吃食物关系
        rels_doeat = []  # 疾病－宜吃食物关系
        rels_recommandeat = []  # 疾病－推荐吃食物关系
        rels_commonddrug = []  # 疾病－通用药品关系
        rels_recommanddrug = []  # 疾病－热门药品关系
        rels_check = []  # 疾病－检查关系
        rels_drug_producer = []  # 品牌药－药物名关系
        rels_symptom = []  # 疾病症状关系
        rels_acompany = []  # 疾病并发关系
        rels_category = []  # 疾病所在的小科室 eg ['肺气肿', '呼吸内科'] 疾病-小科室

        count = 0
        for data in open(self.data_path):
            disease_dict = {}
            count += 1
            # print(count)
            try:
                data_json = json.loads(data)
                disease = data_json['name']
                disease_dict['name'] = disease
                diseases.append(disease)
                disease_dict['desc'] = ''
                disease_dict['prevent'] = ''
                disease_dict['cause'] = ''
                disease_dict['easy_get'] = ''
                disease_dict['cure_department'] = ''
                disease_dict['cure_way'] = ''
                disease_dict['cure_lasttime'] = ''
                disease_dict['symptom'] = ''
                disease_dict['cured_prob'] = ''

                if 'symptom' in data_json:
                    symptoms += data_json['symptom']
                    for symptom in data_json['symptom']:
                        rels_symptom.append([disease, symptom])

                if 'acompany' in data_json:
                    for acompany in data_json['acompany']:
                        rels_acompany.append([disease, acompany])

                if 'desc' in data_json:
                    disease_dict['desc'] = data_json['desc']

                if 'prevent' in data_json:
                    disease_dict['prevent'] = data_json['prevent']

                if 'cause' in data_json:
                    disease_dict['cause'] = data_json['cause']

                if 'get_prob' in data_json:
                    disease_dict['get_prob'] = data_json['get_prob']

                if 'easy_get' in data_json:
                    disease_dict['easy_get'] = data_json['easy_get']

                if 'cure_department' in data_json:
                    cure_department = data_json['cure_department']
                    if len(cure_department) == 1:
                        rels_category.append([disease, cure_department[0]])
                    if len(cure_department) == 2:
                        big = cure_department[0]
                        small = cure_department[1]
                        rels_department.append([small, big])
                        rels_category.append([disease, small])
                    if len(cure_department) == 3:
                        big = cure_department[0]
                        small = cure_department[2]
                        rels_department.append([small, big])
                        rels_category.append([disease, small])
                    if len(cure_department) == 3:
                        big = cure_department[0]
                        small = cure_department[1]
                        rels_department.append([small, big])
                        rels_category.append([disease, small])
                    disease_dict['cure_department'] = cure_department
                    departments += cure_department

                if 'cure_way' in data_json:
                    disease_dict['cure_way'] = data_json['cure_way']

                if 'cure_lasttime' in data_json:
                    disease_dict['cure_lasttime'] = data_json['cure_lasttime']

                if 'cured_prob' in data_json:
                    disease_dict['cured_prob'] = data_json['cured_prob']

                if 'common_drug' in data_json:
                    common_drug = data_json['common_drug']
                    for drug in common_drug:
                        rels_commonddrug.append([disease, drug])
                    drugs += common_drug

                if 'recommand_drug' in data_json:
                    recommand_drug = data_json['recommand_drug']
                    drugs += recommand_drug
                    for drug in recommand_drug:
                        rels_recommanddrug.append([disease, drug])

                if 'not_eat' in data_json:
                    not_eat = data_json['not_eat']
                    for _not in not_eat:
                        rels_noteat.append([disease, _not])

                    foods += not_eat
                    do_eat = data_json['do_eat']
                    for _do in do_eat:
                        rels_doeat.append([disease, _do])

                    foods += do_eat
                    recommand_eat = data_json['recommand_eat']

                    for _recommand in recommand_eat:
                        rels_recommandeat.append([disease, _recommand])
                    foods += recommand_eat

                if 'check' in data_json:
                    check = data_json['check']
                    for _check in check:
                        rels_check.append([disease, _check])
                    checks += check
                if 'drug_detail' in data_json:
                    drug_detail = data_json['drug_detail']
                    producer = [i.split('(')[0] for i in drug_detail]
                    rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
                    producers += producer
                disease_infos.append(disease_dict)
            except:
                print(f"JSON解析错误: {count}")
                continue

        for data in open('/home/gujk/kg-QA/kg-app/medical_knowledge_graph_app-master-master/kg/data/hospital.json'):
                    data_org = eval(data)
                    for i in range(len(data_org)):
                        data_json=data_org [i]
                        doctors_dict={}
                        if 'orgName' in data_json:
                            hospitals.append(data_json['orgName'])
                            departments.append(data_json['ctDeptName'])
                            doctors_dict['empName']=data_json['empName']
                            doctors_dict['orgName']=data_json['orgName']
                            # Create relationships between doctors, departments, and hospitals
                            doctor_department_relations.append([data_json['empName'], data_json['ctDeptName']])
                            department_hospital_relations.append([data_json['ctDeptName'], data_json['orgName']])
                            doctors_and_hospitals.append(doctors_dict)

        return set(drugs), set(foods), set(checks), set(departments), set(producers), set(symptoms), set(diseases), \
               disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, \
               rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category, set(hospitals),  \
               doctor_department_relations, department_hospital_relations,doctors_and_hospitals

    '''建立节点（一般节点，除了节点名称，没有别的属性）'''

    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(label,count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''

    def create_diseases_nodes(self, disease_infos):
        count = 0
        for disease_dict in disease_infos:
            # 创建疾病节点，这个节点包含很多属性。比如描述、预防、易感人群、治愈概率等。
            node = Node("Disease", name=disease_dict['name'], desc=disease_dict['desc'],
                        prevent=disease_dict['prevent'], cause=disease_dict['cause'],
                        easy_get=disease_dict['easy_get'], cure_lasttime=disease_dict['cure_lasttime'],
                        cure_department=disease_dict['cure_department']
                        , cure_way=disease_dict['cure_way'], cured_prob=disease_dict['cured_prob'])
            self.g.create(node)
            count += 1
            print(disease_dict['name'],count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_doctor_nodes(self, doctors_and_hospitals):
        count = 0
        for doctor_info in doctors_and_hospitals:
            doctor_name = doctor_info["empName"]
            working_hospital = doctor_info["orgName"]
            node = Node("Doctors", name=doctor_name, working_hospital=working_hospital)
            self.g.create(node)
            count += 1
            print("Doctors", count, len(doctors_and_hospitals))
    def create_graphnodes(self):
        # 拿到所有实体 和 所有关系的list
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category,Hospitals, \
               doctor_department_relations, department_hospital_relations,doctors_and_hospitals= self.read_nodes()
        self.create_node('Hospitals', Hospitals) # 重新创建症状节点
        self.create_doctor_nodes(doctors_and_hospitals)
        self.create_diseases_nodes(disease_infos)

        self.create_node('Drug', Drugs)
        # print(len(Drugs))
        self.create_node('Food', Foods)
        # print(len(Foods))
        self.create_node('Check', Checks)
        # print(len(Checks))
        self.create_node('Department', Departments)
        # print(len(Departments))
        self.create_node('Producer', Producers)
        # print(len(Producers))
        self.create_node('Symptom', Symptoms) # 重新创建症状节点

        return

    '''创建实体关系边'''

    def create_graphrels(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category,Hospitals, \
               doctor_department_relations, department_hospital_relations,doctors_and_hospitals= self.read_nodes()
        # self.create_relationship('Doctors', 'Department', doctor_department_relations, 'works_in', '工作科室')
        # self.create_relationship('Department', 'Hospitals', department_hospital_relations, 'belongs_to', '属于')
        # self.create_relationship('Disease', 'Food', rels_recommandeat, 'recommand_eat', '推荐食谱')
        # self.create_relationship('Disease', 'Food', rels_noteat, 'no_eat', '忌吃')
        # self.create_relationship('Disease', 'Food', rels_doeat, 'do_eat', '宜吃')
        # self.create_relationship('Department', 'Department', rels_department, 'belongs_to', '属于')
        # self.create_relationship('Disease', 'Drug', rels_commonddrug, 'common_drug', '常用药品')
        # self.create_relationship('Producer', 'Drug', rels_drug_producer, 'drugs_of', '生产药品')
        # self.create_relationship('Disease', 'Drug', rels_recommanddrug, 'recommand_drug', '推荐药品')
        # self.create_relationship('Disease', 'Check', rels_check, 'need_check', '诊断检查')
        # self.create_relationship('Disease', 'Symptom', rels_symptom, 'has_symptom', '症状')  # 创建疾病-症状 的关系
        # self.create_relationship('Disease', 'Disease', rels_acompany, 'acompany_with', '并发症')
        # self.create_relationship('Disease', 'Department', rels_category, 'belongs_to', '所属科室')



    '''创建实体关联边'''

    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]  # 比如疾病名
            q = edge[1]  # 比如症状名
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (start_node, end_node, p, q, rel_type, rel_name)
            # eg. match(p:'Disease'),(q:'Symptom') where p.name = '疾病名' and q.name = '症状名' create (p)-[rel:has_symptom{name:'症状'}]->(q)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''

    def export_data(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category,Hospitals, \
        doctor_department_relations, department_hospital_relations,doctors_and_hospitals = self.read_nodes()
        f_drug = open('drug.txt', 'w+')
        f_food = open('food.txt', 'w+')
        f_check = open('check.txt', 'w+')
        f_department = open('department.txt', 'w+')
        f_producer = open('producer.txt', 'w+')
        f_symptom = open('symptoms.txt', 'w+')
        f_disease = open('disease.txt', 'w+')
        f_doctors=open('doctors.txt', 'w+')
        f_hospitals=open('hospitals.txt', 'w+')

        f_drug.write('\n'.join(list(Drugs)))
        f_food.write('\n'.join(list(Foods)))
        f_check.write('\n'.join(list(Checks)))
        f_department.write('\n'.join(list(Departments)))
        f_producer.write('\n'.join(list(Producers)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))
        f_hospitals.write('\n'.join(list(Hospitals)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_department.close()
        f_producer.close()
        f_symptom.close()
        f_disease.close()
        f_doctors.close()
        f_hospitals.close()


        return


if __name__ == '__main__':
    # 从头到尾构建一遍kg需要3h.
    # 重新执行函数前要把当前的图数据库整个删掉，不然会重复创建一个kg出来。
    # 先清空原来的图数据库（kg）,直接删除data文件夹下的databeses和transactions 版本neo4j 4.1.4
    # 初始密码 neo4j/neo4j
    handler = MedicalGraph()
    # print("step1:导入图谱节点中")
    # handler.create_graphnodes()  # 创建图谱节点
    print("step2:导入图谱边中")
    handler.create_graphrels()  # 创建图谱边

    # 记录创建一次时长，20210820-18：17开始，
