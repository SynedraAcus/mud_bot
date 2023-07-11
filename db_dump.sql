--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Debian 15.3-1.pgdg120+1)
-- Dumped by pg_dump version 15.3 (Debian 15.3-1.pgdg120+1)

-- Started on 2023-07-11 11:15:47 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3400 (class 1262 OID 16384)
-- Name: bot_info; Type: DATABASE; Schema: -; Owner: example_db_user
--

CREATE DATABASE bot_info IF NOT EXISTS WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE bot_info OWNER TO example_db_user;

\connect bot_info

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 223 (class 1259 OID 16430)
-- Name: actions; Type: TABLE; Schema: public; Owner: example_db_user
--

CREATE TABLE public.actions (
    action_id integer NOT NULL,
    scene_id integer,
    keywords text,
    check_id integer,
    description_s text,
    description_f text
);


ALTER TABLE public.actions OWNER TO example_db_user;

--
-- TOC entry 222 (class 1259 OID 16429)
-- Name: actions_action_id_seq; Type: SEQUENCE; Schema: public; Owner: example_db_user
--

ALTER TABLE public.actions ALTER COLUMN action_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.actions_action_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 221 (class 1259 OID 16412)
-- Name: additionals; Type: TABLE; Schema: public; Owner: example_db_user
--

CREATE TABLE public.additionals (
    additional_id integer NOT NULL,
    additional_text text,
    check_id integer,
    scene_id integer
);


ALTER TABLE public.additionals OWNER TO example_db_user;

--
-- TOC entry 220 (class 1259 OID 16411)
-- Name: additionals_additional_id_seq; Type: SEQUENCE; Schema: public; Owner: example_db_user
--

ALTER TABLE public.additionals ALTER COLUMN additional_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.additionals_additional_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 217 (class 1259 OID 16398)
-- Name: checks; Type: TABLE; Schema: public; Owner: example_db_user
--

CREATE TABLE public.checks (
    check_id integer NOT NULL,
    check_type character varying(32),
    variable character varying(32),
    compare_against character varying(32)
);


ALTER TABLE public.checks OWNER TO example_db_user;

--
-- TOC entry 216 (class 1259 OID 16397)
-- Name: checks_check_id_seq; Type: SEQUENCE; Schema: public; Owner: example_db_user
--

ALTER TABLE public.checks ALTER COLUMN check_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.checks_check_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 225 (class 1259 OID 16454)
-- Name: commands; Type: TABLE; Schema: public; Owner: example_db_user
--

CREATE TABLE public.commands (
    command_id integer NOT NULL,
    variable character varying(32),
    new_value character varying(32),
    action_id integer,
    command_type character varying(32)
);


ALTER TABLE public.commands OWNER TO example_db_user;

--
-- TOC entry 224 (class 1259 OID 16453)
-- Name: commands_command_id_seq; Type: SEQUENCE; Schema: public; Owner: example_db_user
--

ALTER TABLE public.commands ALTER COLUMN command_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.commands_command_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 215 (class 1259 OID 16390)
-- Name: placeholders; Type: TABLE; Schema: public; Owner: example_db_user
--

CREATE TABLE public.placeholders (
    placeholder_id integer NOT NULL,
    description text NOT NULL,
    additional_desc text
);


ALTER TABLE public.placeholders OWNER TO example_db_user;

--
-- TOC entry 214 (class 1259 OID 16389)
-- Name: placeholders_placeholder_id_seq; Type: SEQUENCE; Schema: public; Owner: example_db_user
--

ALTER TABLE public.placeholders ALTER COLUMN placeholder_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.placeholders_placeholder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 16404)
-- Name: scenes; Type: TABLE; Schema: public; Owner: example_db_user
--

CREATE TABLE public.scenes (
    scene_id integer NOT NULL,
    scene_identifier character varying(32),
    description text
);


ALTER TABLE public.scenes OWNER TO example_db_user;

--
-- TOC entry 218 (class 1259 OID 16403)
-- Name: scenes_scene_id_seq; Type: SEQUENCE; Schema: public; Owner: example_db_user
--

ALTER TABLE public.scenes ALTER COLUMN scene_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.scenes_scene_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3392 (class 0 OID 16430)
-- Dependencies: 223
-- Data for Name: actions; Type: TABLE DATA; Schema: public; Owner: example_db_user
--

COPY public.actions (action_id, scene_id, keywords, check_id, description_s, description_f) FROM stdin;
1	1	ю;юг	\N	\N	\N
2	1	с;север	\N		
3	2	ю;юг	\N		
4	2	с;север	\N		На то он и северный конец, что дальше на север идти нельзя.
5	2	взять;подобрать;забрать	1	Вы берёте монтировку в руку и сразу чувствуете себя увереннее.	Брать тут больше нечего.
6	3	с;север	\N		
7	3	ю;юг	\N		
8	4	убрать;расчистить;очистить;отодвинуть	6	Вам удалось отвалить несколько камней, и теперь тут можно пролезть.	Голыми руками их точно не сдвинуть с места.
9	4	с;север	\N		
10	4	ю;юг	7	Обдирая колени, вы пролазите под плитой.	Коридор всё ещё завален, и пройти тут нельзя.
\.


--
-- TOC entry 3390 (class 0 OID 16412)
-- Dependencies: 221
-- Data for Name: additionals; Type: TABLE DATA; Schema: public; Owner: example_db_user
--

COPY public.additionals (additional_id, additional_text, check_id, scene_id) FROM stdin;
1	На полу валяется монтировка. Пригодится на случай встречи с хэдкрабами или запертыми дверями.	1	2
2	Под одной из плит виднеется узкий лаз.	4	4
3	Кажется, если их не убрать — пройти не получится.	5	4
\.


--
-- TOC entry 3386 (class 0 OID 16398)
-- Dependencies: 217
-- Data for Name: checks; Type: TABLE DATA; Schema: public; Owner: example_db_user
--

COPY public.checks (check_id, check_type, variable, compare_against) FROM stdin;
1	not_exists	has_crowbar	\N
2	more_or_equal	nonexistent	10
3	not_exists	has_crowbar	\N
4	equals	cleared_rocks	True
5	not_exists	cleared_rocks	\N
6	equals	has_crowbar	True
7	equals	cleared_rocks	True
\.


--
-- TOC entry 3394 (class 0 OID 16454)
-- Dependencies: 225
-- Data for Name: commands; Type: TABLE DATA; Schema: public; Owner: example_db_user
--

COPY public.commands (command_id, variable, new_value, action_id, command_type) FROM stdin;
1	\N	south	1	set_scene
2	\N	north	2	set_scene
3	\N	start	3	set_scene
4	has_crowbar	True	5	set_var
5	\N	start	6	set_scene
6	\N	rocks	7	set_scene
7	cleared_rocks	True	8	set_var
8	\N	south	9	set_scene
9	\N	final	10	set_scene
\.


--
-- TOC entry 3384 (class 0 OID 16390)
-- Dependencies: 215
-- Data for Name: placeholders; Type: TABLE DATA; Schema: public; Owner: example_db_user
--

COPY public.placeholders (placeholder_id, description, additional_desc) FROM stdin;
1	First description ever	
2	Yet another description	Additional lines #2
3	This is the third description	Third set\\nof additional lines
\.


--
-- TOC entry 3388 (class 0 OID 16404)
-- Dependencies: 219
-- Data for Name: scenes; Type: TABLE DATA; Schema: public; Owner: example_db_user
--

COPY public.scenes (scene_id, scene_identifier, description) FROM stdin;
1	start	Вы стоите в коридоре, простирающемся с севера на юг.
2	north	Вы стоите в северном конце коридора.
3	south	Вы стоите в южном конце коридора. Потолок перекошен, а чуть южнее проход вообще завален.
4	rocks	Коридор завален камнями и бетонными плитами.
5	final	К сожалению, нормальное количество контента будет добавлено когда-нибудь потом. На данный момент это конец.
\.


--
-- TOC entry 3401 (class 0 OID 0)
-- Dependencies: 222
-- Name: actions_action_id_seq; Type: SEQUENCE SET; Schema: public; Owner: example_db_user
--

SELECT pg_catalog.setval('public.actions_action_id_seq', 10, true);


--
-- TOC entry 3402 (class 0 OID 0)
-- Dependencies: 220
-- Name: additionals_additional_id_seq; Type: SEQUENCE SET; Schema: public; Owner: example_db_user
--

SELECT pg_catalog.setval('public.additionals_additional_id_seq', 3, true);


--
-- TOC entry 3403 (class 0 OID 0)
-- Dependencies: 216
-- Name: checks_check_id_seq; Type: SEQUENCE SET; Schema: public; Owner: example_db_user
--

SELECT pg_catalog.setval('public.checks_check_id_seq', 7, true);


--
-- TOC entry 3404 (class 0 OID 0)
-- Dependencies: 224
-- Name: commands_command_id_seq; Type: SEQUENCE SET; Schema: public; Owner: example_db_user
--

SELECT pg_catalog.setval('public.commands_command_id_seq', 9, true);


--
-- TOC entry 3405 (class 0 OID 0)
-- Dependencies: 214
-- Name: placeholders_placeholder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: example_db_user
--

SELECT pg_catalog.setval('public.placeholders_placeholder_id_seq', 3, true);


--
-- TOC entry 3406 (class 0 OID 0)
-- Dependencies: 218
-- Name: scenes_scene_id_seq; Type: SEQUENCE SET; Schema: public; Owner: example_db_user
--

SELECT pg_catalog.setval('public.scenes_scene_id_seq', 5, true);


--
-- TOC entry 3233 (class 2606 OID 16452)
-- Name: actions action_action_id_pk; Type: CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT action_action_id_pk PRIMARY KEY (action_id);


--
-- TOC entry 3231 (class 2606 OID 16418)
-- Name: additionals additionals_pkey; Type: CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.additionals
    ADD CONSTRAINT additionals_pkey PRIMARY KEY (additional_id);


--
-- TOC entry 3227 (class 2606 OID 16402)
-- Name: checks checks_pkey; Type: CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.checks
    ADD CONSTRAINT checks_pkey PRIMARY KEY (check_id);


--
-- TOC entry 3235 (class 2606 OID 16458)
-- Name: commands commands_pkey; Type: CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_pkey PRIMARY KEY (command_id);


--
-- TOC entry 3225 (class 2606 OID 16396)
-- Name: placeholders placeholders_pkey; Type: CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.placeholders
    ADD CONSTRAINT placeholders_pkey PRIMARY KEY (placeholder_id);


--
-- TOC entry 3229 (class 2606 OID 16410)
-- Name: scenes scenes_pkey; Type: CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.scenes
    ADD CONSTRAINT scenes_pkey PRIMARY KEY (scene_id);


--
-- TOC entry 3238 (class 2606 OID 16440)
-- Name: actions actions_check_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_check_id_fkey FOREIGN KEY (check_id) REFERENCES public.checks(check_id);


--
-- TOC entry 3239 (class 2606 OID 16435)
-- Name: actions actions_scene_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.actions
    ADD CONSTRAINT actions_scene_id_fkey FOREIGN KEY (scene_id) REFERENCES public.scenes(scene_id);


--
-- TOC entry 3236 (class 2606 OID 16419)
-- Name: additionals additionals_check_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.additionals
    ADD CONSTRAINT additionals_check_id_fkey FOREIGN KEY (check_id) REFERENCES public.checks(check_id);


--
-- TOC entry 3237 (class 2606 OID 16424)
-- Name: additionals additionals_scene_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.additionals
    ADD CONSTRAINT additionals_scene_id_fkey FOREIGN KEY (scene_id) REFERENCES public.scenes(scene_id);


--
-- TOC entry 3240 (class 2606 OID 16459)
-- Name: commands commands_action_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: example_db_user
--

ALTER TABLE ONLY public.commands
    ADD CONSTRAINT commands_action_id_fkey FOREIGN KEY (action_id) REFERENCES public.actions(action_id);


-- Completed on 2023-07-11 11:15:48 UTC

--
-- PostgreSQL database dump complete
--


