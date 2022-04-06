------------------------------------------------------------
-- Table: Region
------------------------------------------------------------
CREATE TABLE public.Region(
	Code_insee   INT  NOT NULL ,
	Nom_region   VARCHAR (50) NOT NULL  ,
	CONSTRAINT Region_PK PRIMARY KEY (Code_insee)
)WITHOUT OIDS;
------------------------------------------------------------
-- Table: Consommation
------------------------------------------------------------
CREATE TABLE public.Consommation(
	Id_conso                   INT  NOT NULL ,
	Consommation_gaz           FLOAT  NOT NULL ,
	Consommation_electricite   FLOAT  NOT NULL  ,
	CONSTRAINT Consommation_PK PRIMARY KEY (Id_conso)
)WITHOUT OIDS;
------------------------------------------------------------
-- Table: Temperature
------------------------------------------------------------
CREATE TABLE public.Temperature(
	Id_temperature   INT  NOT NULL ,
	T_moyenne        FLOAT  NOT NULL ,
	T_minimale       FLOAT  NOT NULL ,
	T_maximale       FLOAT  NOT NULL  ,
	CONSTRAINT Temperature_PK PRIMARY KEY (Id_temperature)
)WITHOUT OIDS;
------------------------------------------------------------
-- Table: Relation
------------------------------------------------------------
CREATE TABLE public.Relation(
	Code_insee       INT  NOT NULL ,
	Id_conso         INT  NOT NULL ,
	Id_temperature   INT  NOT NULL ,
	Date             DATE  NOT NULL  ,
	CONSTRAINT Relation_PK PRIMARY KEY (Code_insee,Id_conso,Id_temperature)

	,CONSTRAINT Relation_Region_FK 
	FOREIGN KEY (Code_insee) 
	REFERENCES public.Region(Code_insee)
	
	,CONSTRAINT Relation_Consommation0_FK 
	FOREIGN KEY (Id_conso) 
	REFERENCES public.Consommation(Id_conso)
	
	,CONSTRAINT Relation_Temperature1_FK 
	FOREIGN KEY (Id_temperature) 
	REFERENCES public.Temperature(Id_temperature)
)WITHOUT OIDS;
