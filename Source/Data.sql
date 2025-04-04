--Metadata for books table
DROP TABLE IF EXISTS "public"."books";
CREATE TABLE "public"."books" (
    "id" int8 NOT NULL DEFAULT nextval('books_id_seq'::regclass),
        "title" varchar(255) NOT NULL,
            "author" varchar(255) NOT NULL,
                "genre" varchar(255) NOT NULL,
                    "year_published" int8 NOT NULL,
                        "summary" text,
                            PRIMARY KEY ("id")
                            );
							
--Metadata for review books table

DROP TABLE IF EXISTS "public"."reviews";


CREATE SEQUENCE IF NOT EXISTS reviews_id_seq;

CREATE TABLE "public"."reviews" (
    "id" int4 NOT NULL DEFAULT nextval('reviews_id_seq'::regclass),
    "book_id" int4 NOT NULL,
    "user_id" int4 NOT NULL,
    "review_text" text NOT NULL,
    "rating" int4 CHECK ((rating >= 1) AND (rating <= 5)),
    PRIMARY KEY ("id")
);

CREATE SEQUENCE IF NOT EXISTS users_id_seq;

--Metadata for user table

CREATE TABLE "public"."users" (
    "id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    "username" varchar(50) NOT NULL,
    "email" varchar(255) NOT NULL,
    "created_at" timestamp DEFAULT CURRENT_TIMESTAMP,
    "hashed_password" varchar NOT NULL,
    PRIMARY KEY ("id")
);

--Insert records to book table
INSERT INTO books (id, title, author, genre, year_published, summary) VALUES
(1, 'Ponniyin Selvan', 'Kalki Krishnamurthy', 'Historical Fiction', 1955, 'Chola era history'),
(2, 'Velpari', 'Su. Venkatesan', 'Historical Fiction', 2018, 'Story of King Pari'),
(3, 'Sivagamiyin Sabatham', 'Kalki Krishnamurthy', 'Historical Fiction', 1948, 'Pallava era story'),
(4, 'Mahabharatham', 'Vyasar', 'Epic', -400, 'Kurukshetra War'),
(5, 'Ramayanam', 'Valmiki', 'Epic', -500, 'Story of Rama'),
(6, 'Silappathikaram', 'Ilango Adigal', 'Epic', 200, 'Story of Kovalan and Kannagi'),
(7, 'Manimekalai', 'Seethalai Saathanar', 'Epic', 600, 'Story of Manimekalai'),
(8, 'Thirukkural', 'Thiruvalluvar', 'Didactic Literature', 400, 'Code of Ethics'),
(9, 'Yayati', 'V. S. Khandekar', 'Novel', 1959, 'Yayatis desire'),
(10, 'Agni Siragugal', 'A. P. J. Abdul Kalam', 'Autobiography', 1999, 'Kalams life story'),
(11, 'Siruthai', 'Su. Abdul Hameed', 'Novel', 2012, 'Life of Tribals'),
(12, 'Gopallapurathu Makkal', 'Ki. Rajanarayanan', 'Novel', 1976, 'Village life'),
(13, 'Anjaadi', 'Poomani', 'Novel', 2013, 'Village politics'),
(14, 'Kaaval Kottam', 'Su. Venkatesan', 'Historical Fiction', 2008, 'Madurai history'),
(15, 'Oru Puliyamarathin Kathai', 'Sundara Ramasamy', 'Novel', 1966, 'Social changes'),
(16, 'Thalaimuraigal', 'Neela. Padmanabhan', 'Novel', 1968, 'Family relationships'),
(17, 'Karippu Manal', 'Na. Parthasarathy', 'Novel', 1971, 'Seaside village'),
(18, 'Saayavanam', 'S. Kandasamy', 'Novel', 1968, 'Workers life'),
(19, 'Vishnupuram', 'Jeyamohan', 'Novel', 1997, 'Indian philosophy'),
(20, 'Kottravai', 'Jeyamohan', 'Novel', 2024, 'Gods and Society'),
(21, 'Panchali Sabatham', 'Subramania Bharati', 'Epic', 1912, 'Mahabharata story'),
(22, 'Veerapandiya Kattabomman', 'Sakthi Kannan', 'Historical Drama', 1959, 'Kattabommans history'),
(23, 'Ratchagan', 'Sandilyan', 'Historical Fiction', 1964, 'Chola era story'),
(24, 'Udaiyaar', 'Balakumaran', 'Historical Fiction', 2002, 'Raja Raja Chola'),
(25, 'Kallikkattu Ithikasam', 'Vairamuthu', 'Novel', 2000, 'Village life'),
(26, 'Kagitha Pookkal', 'Ashokamitran', 'Novel', 1991, 'Middle-class life'),
(27, 'Koolamadevi', 'Chandra', 'Novel', 2019, 'Womens life'),
(28, 'Veril Pazhutha Pala', 'Su. Samuthiram', 'Novel', 1990, 'Social issues'),
(29, 'Karisal Kathaigal', 'Ki. Rajanarayanan', 'Short Stories', 1982, 'Village stories'),
(30, 'Viduthalai', 'C. S. Chellappa', 'Novel', 1954, 'Freedom struggle'),
(31, 'Antharangam', 'Jayakanthan', 'Novel', 1964, 'Human emotions'),
(32, 'Amma Vanthaal', 'Thi. Janakiraman', 'Novel', 1966, 'Family relationships'),
(33, 'Mohamul', 'Thi. Janakiraman', 'Novel', 1951, 'Love story'),
(34, 'Padmavathi Sarithiram', 'A. Madhaviah', 'Novel', 1898, 'Social criticism'),
(35, 'Oru Kudumbam Sithaigirathu', 'Lakshmi', 'Novel', 1966, 'Family relationships'),
(36, 'Suthanthira Thaagam', 'C.S. Chellappa', 'Novel', 2001, 'Freedom Struggle History'),
(37, 'Kallan', 'Mu. Varadarajan', 'Novel', 1950, 'Rural life'),
(38, 'Alaigal', 'Sivasankari', 'Novel', 1983, 'Womens life'),
(39, 'Paarukku Povom', 'Sujatha Rangarajan', 'Novel', 1977, 'Humorous story'),
(40, 'En Peyar Ramaseshan', 'B. V. R.', 'Novel', 1951, 'Social story'),
(41, 'Verum Vizhudhum', 'Na. Parthasarathy', 'Novel', 1965, 'Social story'),
(42, 'Kurinji Then', 'Na. Parthasarathy', 'Novel', 1961, 'Love story'),
(43, 'Poimmaigal', 'Jayakanthan', 'Short Stories', 1965, 'Social stories'),
(44, 'Thozhargal', 'P. Kesavadev', 'Novel', 1954, 'Social relationships'),
(45, 'Chemmeen', 'Thakazhi Sivasankara Pillai', 'Novel', 1956, 'Life of fishermen'),
(46, 'Kayar', 'Thakazhi Sivasankara Pillai', 'Novel', 1978, 'Feudal society'),
(51, 'The White Tiger', 'Aravind Adiga', 'Fiction', 2008, 'Socio-political commentary on modern India'),
(52, 'Life of Pi', 'Yann Martel', 'Adventure Fiction', 2001, 'A boys survival journey with a tiger'),
(53, 'A Suitable Girl', 'Vikram Seth', 'Fiction', 2016, 'A young womans search for a husband'),
(54, 'The God of Small Things', 'Arundhati Roy', 'Fiction', 1997, 'Family secrets and societal constraints in Kerala'),
(55, 'Interpreter of Maladies', 'Jhumpa Lahiri', 'Short Stories', 1999, 'Stories exploring the lives of Indian immigrants'),
(56, 'The Namesake', 'Jhumpa Lahiri', 'Fiction', 2003, 'A Bengali familys assimilation into American culture'),
(57, 'Maximum City: Bombay Lost and Found', 'Suketu Mehta', 'Non-fiction', 2004, 'An in-depth look at the city of Mumbai'),
(58, 'Sacred Games', 'Vikram Chandra', 'Crime Fiction', 2006, 'A complex crime thriller set in Mumbai'),
(59, 'Narcopolis', 'Jeet Thayil', 'Fiction', 2012, 'Exploration of the opium underworld in Mumbai'),
(60, 'Selection Day', 'Aravind Adiga', 'Fiction', 2016, 'Story of two brothers and their cricketing ambitions'),
(61, 'The Inheritance of Loss', 'Kiran Desai', 'Fiction', 2006, 'Intertwining stories of characters in India and the US'),
(62, 'Family Life', 'Akhil Sharma', 'Fiction', 2014, 'A familys immigration from India to the US and tragedy'),
(97, 'Divergent', 'Veronica Roth', 'Young Adult', 2011, 'A dystopian society divided into factions'),
(98, 'The Hunger Games', 'Suzanne Collins', 'Young Adult', 2008, 'A dystopian competition where teenagers fight to the death'),
(100, 'The Kite Runner', 'Khaled Hosseini', 'Fiction', 2003, 'Friendship and betrayal in Afghanistan'),
(63, 'Half of a Yellow Sun', 'Chimamanda Ngozi Adichie', 'Historical Fiction', 2006, 'The Biafran War in Nigeria'),
(81, 'Between the World and Me', 'Ta-Nehisi Coates', 'Non-fiction', 2015, 'A letter to the authors son about race in America'),
(82, 'The Underground Railroad', 'Colson Whitehead', 'Historical Fiction', 2016, 'Reimagining the Underground Railroad as a literal railroad'),
(83, 'There There', 'Tommy Orange', 'Fiction', 2018, 'Interconnected stories of Native Americans in Oakland'),
(94, 'The Help', 'Kathryn Stockett', 'Historical Fiction', 2009, 'Relationships between black maids and white families in 1960s Mississippi'),
(78, 'Educated', 'Tara Westover', 'Memoir', 2018, 'A womans journey from a survivalist family to education'),
(47, 'The God of Small Things', 'Arundhati Roy', 'Novel', 1997, 'Family secrets and societal constraints in Kerala'),
(99, 'The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Mystery', 2005, 'A disgraced journalist investigates a family disappearance'),
(48, 'A Suitable Boy', 'Vikram Seth', 'Novel', 1993, 'Indian society'),
(49, 'Midnights Children', 'Salman Rushdie', 'Novel', 1981, 'Indias independence');


--Insert records to review table


INSERT INTO reviews (id, book_id, user_id, review_text, rating) VALUES
(1, 1, 101, 'A masterpiece of historical fiction!', 4.5),
(2, 1, 102, 'The characters are so well-developed.', 5.0),
(3, 2, 103, 'I loved learning about King Pari.', 4.0),
(4, 2, 101, 'A bit slow in some parts, but overall good.', 3.5),
(5, 3, 104, 'The story of Sivagami is captivating.', 4.8),
(6, 3, 102, 'A classic tale of love and revenge.', 5.0),
(7, 4, 105, 'The greatest epic ever written.', 5.0),
(8, 4, 103, 'So many characters to keep track of!', 4.0),
(9, 5, 106, 'Ramas journey is inspiring.', 4.7),
(10, 5, 104, 'A timeless story of good vs. evil.', 5.0),
(11, 6, 107, 'Kannagis devotion is powerful.', 4.9),
(12, 6, 105, 'A tragic love story.', 4.5),
(13, 7, 108, 'Manimekalais path is interesting.', 4.3),
(14, 7, 106, 'A good sequel to Silappathikaram.', 4.0),
(15, 8, 109, 'Words to live by.', 5.0),
(16, 8, 107, 'Thiruvalluvars wisdom is timeless.', 5.0),
(17, 9, 110, 'Yayatis story is a cautionary tale.', 4.2),
(18, 9, 108, 'A thought-provoking novel.', 4.5),
(19, 10, 111, 'Kalams life is truly inspiring.', 5.0),
(20, 10, 109, 'A must-read for every Indian.', 5.0),
(21, 11, 112, 'A powerful portrayal of tribal life.', 4.6),
(22, 11, 110, 'The author writes beautifully about nature.', 4.0),
(23, 12, 113, 'A vivid depiction of village life.', 4.8),
(24, 12, 111, 'I felt like I was there in Gopallapuram.', 5.0),
(25, 13, 101, 'A raw and honest portrayal of village politics.', 4.4),
(26, 13, 112, 'The characters are very realistic.', 4.0),
(27, 14, 102, 'The history of Madurai comes alive.', 4.7),
(28, 14, 113, 'A long but rewarding read.', 4.5),
(29, 15, 103, 'A unique perspective on social change.', 4.3),
(30, 15, 101, 'The symbolism is very effective.', 4.0),
(31, 16, 104, 'A poignant story of family.', 4.5),
(32, 16, 102, 'The author writes with great sensitivity.', 4.2),
(33, 17, 105, 'Life in a seaside village is beautifully captured.', 4.7),
(34, 17, 103, 'The descriptions are very evocative.', 4.0),
(35, 18, 106, 'A powerful portrayal of workers struggles.', 4.9),
(36, 18, 104, 'The authors style is very engaging.', 4.5),
(37, 19, 107, 'An exploration of deep philosophical themes.', 4.4),
(38, 19, 105, 'A challenging but rewarding read.', 4.2),
(39, 20, 108, 'A thought-provoking novel on faith and society', 4.6),
(40, 20, 106, 'Jeyamohans storytelling is masterful', 4.8),
(41, 21, 109, 'Bharatis poetry is inspiring', 5.0),
(42, 21, 107, 'A powerful retelling of a Mahabharata episode', 4.9),
(43, 22, 110, 'A dramatic portrayal of Kattabommans life', 4.7),
(44, 22, 108, 'The historical context is well-researched', 4.5),
(45, 23, 111, 'An entertaining historical adventure', 4.3),
(46, 23, 109, 'Sandilyans writing is captivating', 4.0),
(47, 24, 112, 'A detailed account of Raja Raja Cholas reign', 4.8),
(48, 24, 110, 'Balakumaran brings history to life', 4.6),
(49, 25, 113, 'A moving story of rural life', 4.5),
(50, 25, 111, 'Vairamuthus prose is poetic', 4.2),
(51, 51, 101, 'Aravind Adiga is a brilliant writer.', 4.7),
(52, 51, 102, 'The White Tiger is a must-read for understanding modern India.', 4.9),
(53, 52, 103, 'Life of Pi is a beautiful and imaginative story.', 4.8),
(54, 52, 104, 'The ending is quite thought-provoking.', 4.5),
(55, 53, 105, 'A Suitable Girl provides a fascinating look at Indian society.', 4.6),
(56, 53, 106, 'Vikram Seths writing is so detailed and immersive.', 4.7),
(57, 54, 107, 'The God of Small Things is a masterpiece of language.', 5.0),
(58, 54, 108, 'Arundhati Roys prose is lyrical and evocative.', 4.9),
(59, 55, 109, 'Jhumpa Lahiris short stories are poignant and insightful.', 4.4),
(60, 55, 110, 'Interpreter of Maladies is a great collection.', 4.5),
(61, 56, 111, 'The Namesake is a moving story of identity and belonging.', 4.7),
(62, 56, 112, 'Jhumpa Lahiri writes with such empathy and understanding.', 4.8),
(63, 57, 113, 'Maximum City is a fascinating exploration of Mumbai.', 4.6),
(64, 57, 101, 'Suketu Mehtas book is a must-read for anyone interested in urban life.', 4.5),
(65, 58, 102, 'Sacred Games is a gripping crime thriller.', 4.9),
(66, 58, 103, 'Vikram Chandras characters are complex and compelling.', 4.8),
(67, 59, 104, 'Narcopolis is a dark and atmospheric novel.', 4.7),
(68, 59, 105, 'Jeet Thayils writing is vivid and intense.', 4.6),
(69, 60, 106, 'Selection Day is a powerful story about ambition and family.', 4.8),
(70, 60, 107, 'Aravind Adigas portrayal of modern India is insightful.', 4.9),
(71, 61, 108, 'The Inheritance of Loss is a beautifully written novel.', 4.7),
(72, 61, 109, 'Kiran Desais characters are memorable and complex.', 4.6),
(73, 62, 110, 'Family Life is a moving and poignant story.', 4.5),
(74, 62, 111, 'Akhil Sharmas writing is honest and unflinching.', 4.4),
(75, 97, 101, 'Divergent was an exciting read!', 4.2),
(76, 97, 102, 'I enjoyed the faction system.', 4.0),
(77, 98, 103, 'The Hunger Games kept me on the edge of my seat.', 4.5),
(78, 98, 104, 'Katniss is a great protagonist.', 4.7),
(79, 100, 105, 'The Kite Runner is a heartbreaking story.', 4.9),
(80, 100, 106, 'Khaled Hosseinis writing is so emotional.', 5.0),
(81, 63, 107, 'Half of a Yellow Sun is a powerful historical novel.', 4.8),
(82, 63, 108, 'Adichie is a gifted storyteller.', 4.7),
(83, 81, 109, 'Between the World and Me is an important book.', 4.9),
(84, 81, 110, 'Coates writes with such passion and clarity.', 5.0),
(85, 82, 111, 'The Underground Railroad is a unique and compelling narrative.', 4.6),
(86, 82, 112, 'Whiteheads writing is inventive and thought-provoking.', 4.8),
(87, 83, 113, 'There There offers a powerful perspective on Native American identity.', 4.7),
(88, 83, 101, 'Oranges writing is sharp and insightful.', 4.5),
(89, 94, 102, 'The Help provides a poignant look at a difficult period in history.', 4.4),
(90, 94, 103, 'Stocketts characters are complex and well-drawn.', 4.3),
(91, 78, 104, 'Educated is an inspiring memoir.', 4.8),
(92, 78, 105, 'Westovers journey is remarkable.', 4.9),
(93, 47, 106, 'The God of Small Things is a literary masterpiece.', 5.0),
(94, 47, 107, 'Roys writing is poetic and evocative.', 4.9),
(95, 99, 108, 'The Girl with the Dragon Tattoo is a thrilling mystery.', 4.6),
(96, 99, 109, 'Larssons characters are fascinating.', 4.7),
(97, 48, 110, 'A Suitable Boy is a sprawling and immersive novel.', 4.8),
(98, 48, 111, 'Seths writing is detailed and engaging.', 4.9),
(99, 49, 112, 'Midnights Children is a magical and imaginative story.', 4.7),
(100, 49, 113, 'Rushdies writing is inventive and playful.', 4.8);


--Insert records to user table
INSERT INTO users (id, username, email, created_at, hashed_password) VALUES
(101, 'aravindhan', 'aravindhan@example.com', '2024-07-20 10:00:00', '$2b$12$EXAMPLE_HASHED_PASSWORD1'),
(102, 'malarvizhi', 'malarvizhi1992@email.co.in', '2024-07-20 10:00:00', '$2b$12$EXAMPLE_HASHED_PASSWORD2'),
(103, 'karthik_s', 'karthik.subra@demo.net', '2024-07-21 14:30:00', '$2b$12$EXAMPLE_HASHED_PASSWORD3'),
(104, 'anushya', 'anu.varma@mymail.org', '2024-07-21 14:30:00', '$2b$12$EXAMPLE_HASHED_PASSWORD4'),
(105, 'vijay_k', 'vijaykumar@fastmail.com', '2024-07-22 09:15:00', '$2b$12$EXAMPLE_HASHED_PASSWORD5'),
(106, 'deepika_r', 'deepika.ravi@web.in', '2024-07-22 09:15:00', '$2b$12$EXAMPLE_HASHED_PASSWORD6'),
(107, 'sathish_m', 'sathish.mani@mail.io', '2024-07-23 18:00:00', '$2b$12$EXAMPLE_HASHED_PASSWORD7'),
(108, 'nithya_p', 'nithya123@email.info', '2024-07-23 18:00:00', '$2b$12$EXAMPLE_HASHED_PASSWORD8'),
(109, 'rajesh_nair', 'rajesh.n@sample.com', '2024-07-24 11:00:00', '$2b$12$EXAMPLE_HASHED_PASSWORD9'),
(110, 'priya_dev', 'priya.dev@domain.com', '2024-07-24 11:00:00', '$2b$12$EXAMPLE_HASHED_PASSWORD10'),
(111, 'ranveer', 'ranveer_singh@mail.com', '2024-07-25 16:45:00', '$2b$12$EXAMPLE_HASHED_PASSWORD11'),
(112, 'alia_b', 'alia.bhat@email.net', '2024-07-25 16:45:00', '$2b$12$EXAMPLE_HASHED_PASSWORD12'),
(113, 'mahesh_b', 'mahesh.babu@test.org', '2024-07-26 08:00:00', '$2b$12$EXAMPLE_HASHED_PASSWORD13');
;


CREATE UNIQUE INDEX "Books_pkey" ON public.books USING btree (id);
ALTER TABLE "public"."reviews" ADD FOREIGN KEY ("user_id") REFERENCES "public"."users"("id");
ALTER TABLE "public"."reviews" ADD FOREIGN KEY ("book_id") REFERENCES "public"."books"("id");

CREATE UNIQUE INDEX users_username_key ON public.users USING btree (username);
CREATE UNIQUE INDEX users_email_key ON public.users USING btree (email);
