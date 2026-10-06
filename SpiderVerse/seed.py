from app import app

from models.conn import db

from models.models import Universe, Movie, Character





with app.app_context():



    # ============================================================

    # RESET DATABASE

    # ============================================================



    db.drop_all()

    db.create_all()



    # ============================================================

    # UNIVERSI

    # ============================================================



    raimi = Universe(

        name="Raimi Universe",

        description="La trilogia cinematografica diretta da Sam Raimi con Tobey Maguire.",

        image="raimi.jpg",

        actor="Tobey Maguire"

    )



    amazing = Universe(

        name="The Amazing Spider-Man",

        description="L'universo cinematografico di Spider-Man con Andrew Garfield.",

        image="amazing.jpg",

        actor="Andrew Garfield"

    )



    mcu = Universe(

        name="Marvel Cinematic Universe",

        description="La versione di Spider-Man del Marvel Cinematic Universe interpretata da Tom Holland.",

        image="mcu.jpg",

        actor="Tom Holland"

    )



    spiderverse = Universe(

        name="Spider-Verse",

        description="L'universo animato incentrato su Miles Morales e sul multiverso degli Spider-People.",

        image="spiderverse.jpg",

        actor="Shameik Moore"

    )



    db.session.add_all([

        raimi,

        amazing,

        mcu,

        spiderverse

    ])



    db.session.flush()



    # ============================================================

    # FILM

    # ============================================================



    movies = {



        # RAIMI



        "spiderman_2002": Movie(

            title="Spider-Man",

            year=2002,

            description="Peter Parker viene morso da un ragno geneticamente modificato e diventa Spider-Man.",

            poster="spiderman-2002.jpg",

            duration=121,

            director="Sam Raimi",

            universe=raimi

        ),



        "spiderman_2": Movie(

            title="Spider-Man 2",

            year=2004,

            description="Peter Parker affronta Doctor Octopus mentre cerca di conciliare la propria vita personale con quella da supereroe.",

            poster="spiderman-2.jpg",

            duration=127,

            director="Sam Raimi",

            universe=raimi

        ),



        "spiderman_3": Movie(

            title="Spider-Man 3",

            year=2007,

            description="Peter affronta Sandman, Venom e il lato oscuro provocato dal simbionte.",

            poster="spiderman-3.jpg",

            duration=139,

            director="Sam Raimi",

            universe=raimi

        ),



        # AMAZING



        "amazing_1": Movie(

            title="The Amazing Spider-Man",

            year=2012,

            description="Peter Parker indaga sulla scomparsa dei genitori e affronta Lizard.",

            poster="amazing-2012.jpg",

            duration=136,

            director="Marc Webb",

            universe=amazing

        ),



        "amazing_2": Movie(

            title="The Amazing Spider-Man 2",

            year=2014,

            description="Peter Parker affronta Electro e Green Goblin mentre cerca di proteggere Gwen Stacy.",

            poster="amazing-2.jpg",

            duration=142,

            director="Marc Webb",

            universe=amazing

        ),



        # MCU



        "homecoming": Movie(

            title="Spider-Man: Homecoming",

            year=2017,

            description="Peter Parker cerca di dimostrare di essere un vero Avenger affrontando Vulture.",

            poster="homecoming.jpg",

            duration=133,

            director="Jon Watts",

            universe=mcu

        ),



        "far_from_home": Movie(

            title="Spider-Man: Far From Home",

            year=2019,

            description="Peter parte per l'Europa con la scuola e affronta la minaccia di Mysterio.",

            poster="far-from-home.jpg",

            duration=129,

            director="Jon Watts",

            universe=mcu

        ),



        "no_way_home": Movie(

            title="Spider-Man: No Way Home",

            year=2021,

            description="Un incantesimo di Doctor Strange apre il multiverso facendo arrivare eroi e nemici provenienti da altri universi.",

            poster="no-way-home.jpg",

            duration=148,

            director="Jon Watts",

            universe=mcu

        ),



        "brand_new_day": Movie(

            title="Spider-Man: Brand New Day",

            year=2026,

            description="Peter Parker combatte il crimine a tempo pieno come Spider-Man in un mondo che non ricorda più la sua identità.",

            poster="brand-new-day.jpg",

            duration=145,

            director="Destin Daniel Cretton",

            universe=mcu

        ),



        # SPIDER-VERSE



        "into_spiderverse": Movie(

            title="Spider-Man: Into the Spider-Verse",

            year=2018,

            description="Miles Morales diventa Spider-Man e incontra Spider-People provenienti da universi differenti.",

            poster="into-spider-verse.png",

            duration=117,

            director="Bob Persichetti, Peter Ramsey, Rodney Rothman",

            universe=spiderverse

        ),



        "across_spiderverse": Movie(

            title="Spider-Man: Across the Spider-Verse",

            year=2023,

            description="Miles Morales viaggia attraverso il multiverso e incontra la Spider-Society.",

            poster="across-spider-verse.jpg",

            duration=140,

            director="Joaquim Dos Santos, Kemp Powers, Justin K. Thompson",

            universe=spiderverse

        )

    }



    db.session.add_all(movies.values())

    db.session.flush()



    # ============================================================

    # FUNZIONE PER CREARE PERSONAGGI

    # ============================================================



    def add_character(

        name,

        alias,

        description,

        actor,

        universe,

        movie_keys,

        role="Hero",

        status="Active",

        gender="Male",

        character_type="Human",

        powers="",

        image="default-character.jpg"

    ):



        character = Character(

            name=name,

            alias=alias,

            description=description,

            image=image,

            gender=gender,

            role=role,

            status=status,

            actor=actor,

            type=character_type,

            powers=powers

        )



        character.universes.append(universe)



        for movie_key in movie_keys:

            movies[movie_key].characters.append(character)



        db.session.add(character)



        return character



    # ============================================================

    # RAIMI UNIVERSE

    # ============================================================



    add_character(

        "Peter Parker",

        "Spider-Man",

        "Peter Parker è Spider-Man nell'universo cinematografico di Sam Raimi.",

        "Tobey Maguire",

        raimi,

        ["spiderman_2002", "spiderman_2", "spiderman_3", "no_way_home"],

        powers="Super forza, agilità, senso di ragno, arrampicata sui muri e ragnatele organiche.",

        image="peter-tobey.jpg"

    )



    add_character(

        "Mary Jane Watson",

        "MJ",

        "Amica d'infanzia e principale interesse amoroso di Peter Parker.",

        "Kirsten Dunst",

        raimi,

        ["spiderman_2002", "spiderman_2", "spiderman_3"],

        role="Supporting",

        gender="Female",

        image="mj-tobey.jpg"

    )



    add_character(

        "Harry Osborn",

        "New Goblin",

        "Migliore amico di Peter Parker e figlio di Norman Osborn.",

        "James Franco",

        raimi,

        ["spiderman_2002", "spiderman_2", "spiderman_3"],

        role="Antihero",

        status="Deceased",

        powers="Tecnologia Goblin, forza potenziata, aliante e bombe.",

        image="harry-tobey.jpg"

    )



    add_character(

        "Norman Osborn",

        "Green Goblin",

        "Industriale e scienziato che diventa Green Goblin.",

        "Willem Dafoe",

        raimi,

        ["spiderman_2002", "spiderman_2", "spiderman_3", "no_way_home"],

        role="Villain",

        status="Deceased",

        powers="Forza sovrumana, resistenza, tecnologia avanzata, bombe e aliante.",

        image="goblin.jpg"

    )



    add_character(

        "May Parker",

        "Aunt May",

        "Zia di Peter Parker e una delle persone più importanti della sua vita.",

        "Rosemary Harris",

        raimi,

        ["spiderman_2002", "spiderman_2", "spiderman_3"],

        role="Supporting",

        gender="Female",

        image="may-tobey.jpg"

    )



    add_character(

        "Ben Parker",

        "Uncle Ben",

        "Zio di Peter Parker e figura fondamentale nella nascita di Spider-Man.",

        "Cliff Robertson",

        raimi,

        ["spiderman_2002", "spiderman_2", "spiderman_3"],

        role="Supporting",

        status="Deceased",

        image="ben-tobey.jpg"

    )



    add_character(

        "J. Jonah Jameson",

        "J. Jonah Jameson",

        "Direttore del Daily Bugle e critico costante di Spider-Man.",

        "J.K. Simmons",

        raimi,

        ["spiderman_2002", "spiderman_2", "spiderman_3"],

        role="Supporting",

        image="jj-tobey.jpg"

    )



    add_character(

        "Otto Octavius",

        "Doctor Octopus",

        "Scienziato brillante collegato a quattro tentacoli meccanici intelligenti.",

        "Alfred Molina",

        raimi,

        ["spiderman_2", "no_way_home"],

        role="Villain",

        status="Deceased",

        powers="Quattro tentacoli meccanici, intelligenza scientifica e forza aumentata.",

        image="doc-ock.jpeg"

    )



    add_character(

        "Flint Marko",

        "Sandman",

        "Criminale che acquisisce la capacità di trasformare il proprio corpo in sabbia.",

        "Thomas Haden Church",

        raimi,

        ["spiderman_3", "no_way_home"],

        role="Villain",

        powers="Manipolazione della sabbia, trasformazione corporea, forza e resistenza sovrumane.",

        image="sandman-tobey.jpg"

    )



    add_character(

        "Eddie Brock",

        "Venom",

        "Fotografo rivale di Peter Parker che si unisce al simbionte alieno.",

        "Topher Grace",

        raimi,

        ["spiderman_3"],

        role="Villain",

        status="Deceased",

        character_type="Human / Symbiote",

        powers="Super forza, agilità, ragnatele e capacità del simbionte.",

        image="eddie-tobey.jpg"

    )



    add_character(

        "Gwen Stacy",

        "Gwen Stacy",

        "Compagna universitaria di Peter Parker.",

        "Bryce Dallas Howard",

        raimi,

        ["spiderman_3"],

        role="Supporting",

        gender="Female",

        image="gwen-tobey.jpg"

    )



    # ============================================================

    # THE AMAZING SPIDER-MAN

    # ============================================================



    add_character(

        "Peter Parker",

        "Spider-Man",

        "Peter Parker dell'universo The Amazing Spider-Man.",

        "Andrew Garfield",

        amazing,

        ["amazing_1", "amazing_2", "no_way_home"],

        powers="Super forza, agilità, senso di ragno, arrampicata e ragnatele artificiali.",

        image="peter-andrew.jpg"

    )



    add_character(

        "Gwen Stacy",

        "Gwen Stacy",

        "Studentessa brillante e interesse amoroso di Peter Parker.",

        "Emma Stone",

        amazing,

        ["amazing_1", "amazing_2"],

        role="Supporting",

        status="Deceased",

        gender="Female",

        image="gwen-andrew.jpg"

    )



    add_character(

        "May Parker",

        "Aunt May",

        "Zia di Peter Parker.",

        "Sally Field",

        amazing,

        ["amazing_1", "amazing_2"],

        role="Supporting",

        gender="Female",

        image="may-andrew.jpg"

    )



    add_character(

        "Ben Parker",

        "Uncle Ben",

        "Zio di Peter Parker.",

        "Martin Sheen",

        amazing,

        ["amazing_1"],

        role="Supporting",

        status="Deceased"

    )



    add_character(

        "Curt Connors",

        "Lizard",

        "Scienziato della Oscorp che si trasforma in una gigantesca creatura rettile.",

        "Rhys Ifans",

        amazing,

        ["amazing_1", "no_way_home"],

        role="Villain",

        powers="Forza sovrumana, rigenerazione, agilità e trasformazione rettile.",

        image="lizard-andrew.jpg"

    )



    add_character(

        "George Stacy",

        "Captain Stacy",

        "Capitano della polizia e padre di Gwen Stacy.",

        "Denis Leary",

        amazing,

        ["amazing_1"],

        role="Supporting",

        status="Deceased"

    )



    add_character(

        "Richard Parker",

        "Richard Parker",

        "Padre di Peter Parker e scienziato della Oscorp.",

        "Campbell Scott",

        amazing,

        ["amazing_1", "amazing_2"],

        role="Supporting",

        status="Deceased"

    )



    add_character(

        "Mary Parker",

        "Mary Parker",

        "Madre di Peter Parker.",

        "Embeth Davidtz",

        amazing,

        ["amazing_1", "amazing_2"],

        role="Supporting",

        status="Deceased",

        gender="Female"

    )



    add_character(

        "Rajit Ratha",

        "Dr. Ratha",

        "Dirigente della Oscorp coinvolto nelle ricerche di Curt Connors.",

        "Irrfan Khan",

        amazing,

        ["amazing_1"],

        role="Supporting"

    )



    add_character(

        "Max Dillon",

        "Electro",

        "Dipendente della Oscorp trasformato in un essere capace di controllare l'elettricità.",

        "Jamie Foxx",

        amazing,

        ["amazing_2", "no_way_home"],

        role="Villain",

        powers="Manipolazione dell'elettricità, assorbimento energetico e proiezione di energia.",

        image="electro-andrew.jpg"

    )



    add_character(

        "Harry Osborn",

        "Green Goblin",

        "Figlio di Norman Osborn e vecchio amico di Peter Parker.",

        "Dane DeHaan",

        amazing,

        ["amazing_2"],

        role="Villain",

        powers="Forza potenziata, armatura tecnologica e aliante.",

        image="harry-andrew.jpg"

    )



    add_character(

        "Aleksei Sytsevich",

        "Rhino",

        "Criminale che utilizza una potente armatura meccanizzata.",

        "Paul Giamatti",

        amazing,

        ["amazing_2"],

        role="Villain",

        powers="Armatura meccanica pesante, forza e armi.",

        image="rhino.jpg"

    )



    add_character(

        "Donald Menken",

        "Donald Menken",

        "Dirigente della Oscorp.",

        "Colm Feore",

        amazing,

        ["amazing_2"],

        role="Supporting"

    )



    add_character(

        "Felicia Hardy",

        "Felicia",

        "Assistente di Harry Osborn alla Oscorp.",

        "Felicity Jones",

        amazing,

        ["amazing_2"],

        role="Supporting",

        gender="Female"

    )



    # ============================================================

    # MCU

    # ============================================================



    add_character(

        "Peter Parker",

        "Spider-Man",

        "Spider-Man del Marvel Cinematic Universe.",

        "Tom Holland",

        mcu,

        ["homecoming", "far_from_home", "no_way_home", "brand_new_day"],

        powers="Super forza, agilità, senso di ragno, arrampicata e lancia-ragnatele tecnologici.",

        image="peter-tom.jpg"

    )



    add_character(

        "Michelle Jones-Watson",

        "MJ",

        "Compagna di scuola e interesse amoroso di Peter Parker.",

        "Zendaya",

        mcu,

        ["homecoming", "far_from_home", "no_way_home", "brand_new_day"],

        role="Supporting",

        gender="Female",

        image="mj-tom.jpg"

    )



    add_character(

        "Ned Leeds",

        "Ned",

        "Migliore amico di Peter Parker.",

        "Jacob Batalon",

        mcu,

        ["homecoming", "far_from_home", "no_way_home", "brand_new_day"],

        role="Supporting",

        image="ned-tom.jpg"

    )



    add_character(

        "May Parker",

        "Aunt May",

        "Zia di Peter Parker.",

        "Marisa Tomei",

        mcu,

        ["homecoming", "far_from_home", "no_way_home", "brand_new_day"],

        role="Supporting",

        status="Deceased",

        gender="Female",

        image="may-tom.jpg"

    )



    add_character(

        "Happy Hogan",

        "Happy",

        "Collaboratore di Tony Stark e alleato di Peter Parker.",

        "Jon Favreau",

        mcu,

        ["homecoming", "far_from_home", "no_way_home"],

        role="Supporting",

        image="happy.jpg"

    )



    add_character(

        "Tony Stark",

        "Iron Man",

        "Mentore di Peter Parker e fondatore degli Avengers.",

        "Robert Downey Jr.",

        mcu,

        ["homecoming"],

        role="Hero",

        status="Deceased",

        powers="Armatura Iron Man, intelligenza, armi energetiche e tecnologia avanzata.",

        image="tony.jpg"

    )



    add_character(

        "Adrian Toomes",

        "Vulture",

        "Trafficante di tecnologia aliena che utilizza una tuta volante.",

        "Michael Keaton",

        mcu,

        ["homecoming"],

        role="Villain",

        powers="Tuta alata tecnologica, forza aumentata e armi avanzate.",

        image="adrian.jpg"

    )



    add_character(

        "Herman Schultz",

        "Shocker",

        "Membro dell'organizzazione criminale di Adrian Toomes.",

        "Bokeem Woodbine",

        mcu,

        ["homecoming"],

        role="Villain",

        powers="Guanti tecnologici capaci di produrre potenti onde d'urto."

    )



    add_character(

        "Jackson Brice",

        "Shocker",

        "Membro della squadra di Adrian Toomes e primo utilizzatore dei guanti di Shocker.",

        "Logan Marshall-Green",

        mcu,

        ["homecoming"],

        role="Villain",

        status="Deceased"

    )



    add_character(

        "Aaron Davis",

        "Aaron Davis",

        "Criminale di basso livello e zio di Miles Morales.",

        "Donald Glover",

        mcu,

        ["homecoming"],

        role="Supporting",

        image="aaron.jpg"

    )



    add_character(

        "Quentin Beck",

        "Mysterio",

        "Ex dipendente delle Stark Industries che utilizza illusioni e droni.",

        "Jake Gyllenhaal",

        mcu,

        ["far_from_home"],

        role="Villain",

        status="Deceased",

        powers="Droni armati, illusioni olografiche e tecnologia avanzata.",

        image="mysterio.jpg"

    )



    add_character(

        "Nick Fury",

        "Nick Fury",

        "Direttore dello S.H.I.E.L.D. e alleato degli Avengers.",

        "Samuel L. Jackson",

        mcu,

        ["far_from_home"],

        role="Supporting"

    )



    add_character(

        "Maria Hill",

        "Maria Hill",

        "Agente dello S.H.I.E.L.D.",

        "Cobie Smulders",

        mcu,

        ["far_from_home"],

        role="Supporting",

        gender="Female"

    )



    add_character(

        "Talos",

        "Talos",

        "Skrull che assume temporaneamente l'aspetto di Nick Fury.",

        "Ben Mendelsohn",

        mcu,

        ["far_from_home"],

        role="Supporting",

        character_type="Skrull",

        powers="Mutamento di forma."

    )



    add_character(

        "Soren",

        "Soren",

        "Skrull che assume l'aspetto di Maria Hill.",

        "Sharon Blynn",

        mcu,

        ["far_from_home"],

        role="Supporting",

        gender="Female",

        character_type="Skrull",

        powers="Mutamento di forma."

    )

    add_character(

        "Stephen Strange",

        "Doctor Strange",

        "Maestro delle arti mistiche coinvolto nell'apertura del multiverso.",

        "Benedict Cumberbatch",

        mcu,

        ["no_way_home"],

        role="Hero",

        powers="Magia, portali dimensionali, proiezione astrale e manipolazione mistica.",

        image="docstrange.jpg"

    )



    add_character(

        "Wong",

        "Wong",

        "Stregone Supremo e alleato di Doctor Strange.",

        "Benedict Wong",

        mcu,

        ["no_way_home"],

        role="Hero",

        powers="Magia e arti mistiche."

    )



    add_character(

        "Matt Murdock",

        "Daredevil",

        "Avvocato che aiuta Peter Parker dopo la rivelazione della sua identità.",

        "Charlie Cox",

        mcu,

        ["no_way_home"],

        role="Hero",

        powers="Sensi estremamente sviluppati, combattimento corpo a corpo."

    )



    add_character(

        "J. Jonah Jameson",

        "J. Jonah Jameson",

        "Giornalista del Daily Bugle che rivela pubblicamente l'identità di Spider-Man.",

        "J.K. Simmons",

        mcu,

        ["far_from_home", "no_way_home"],

        role="Supporting"

    )



    add_character(

        "Frank Castle",

        "Punisher",

        "Vigilante che combatte il crimine con metodi estremi.",

        "Jon Bernthal",

        mcu,

        ["brand_new_day"],

        role="Antihero",

        powers="Combattimento, armi da fuoco, tattica e addestramento militare.",

        image="frank.jpg"

    )



    add_character(

        "Bruce Banner",

        "Hulk",

        "Scienziato e membro degli Avengers capace di trasformarsi in Hulk.",

        "Mark Ruffalo",

        mcu,

        ["brand_new_day"],

        role="Hero",

        powers="Super forza, resistenza e trasformazione in Hulk.",

        image="hulk.jpg"

    )



    add_character(

        "Mac Gargan",

        "Scorpion",

        "Criminale già incontrato da Spider-Man nell'MCU.",

        "Michael Mando",

        mcu,

        ["homecoming", "brand_new_day"],

        role="Villain",

        image="scorpion.jpg"

    )


    add_character(

        "Jean Grey",

        "Jean Grey",

        "Mutante dotata di potenti capacità telepatiche e telecinetiche.",

        "Sadie Sink",

        mcu,

        ["brand_new_day"],

        role="Hero",

        gender="Female",

        character_type="Mutant",

        powers="Telepatia, telecinesi e manipolazione psichica.",

        image="jean-grey.jpg"

    )



    add_character(

        "William Metzger",

        "Bill Metzger",

        "Personaggio coinvolto negli eventi di Spider-Man: Brand New Day.",

        "Tramell Tillman",

        mcu,

        ["brand_new_day"],

        role="Supporting",

        image="bill-metzger.jpg"

    )



    add_character(

        "Jean DeWolff",

        "Detective Jean DeWolff",

        "Detective della polizia di New York coinvolta negli eventi di Brand New Day.",

        "Liza Colón-Zayas",

        mcu,

        ["brand_new_day"],

        role="Supporting",

        gender="Female",

        image="jean-dewolff.jpg"

    )



    add_character(

        "Yelena Belova",

        "Black Widow",

        "Agente e combattente altamente addestrata.",

        "Florence Pugh",

        mcu,

        ["brand_new_day"],

        role="Antihero",

        gender="Female",

        powers="Combattimento corpo a corpo, armi e addestramento da agente.",

        image="yelena.jpg"

    )



    add_character(

        "Lonnie Lincoln",

        "Tombstone",

        "Criminale noto come Tombstone.",

        "Marvin Jones III",

        mcu,

        ["brand_new_day"],

        role="Villain",

        powers="Forza e resistenza fisica elevate.",

        image="tombstone-mcu.jpg"

    )



    # ============================================================

    # SPIDER-VERSE

    # ============================================================



    add_character(

        "Miles Morales",

        "Spider-Man",

        "Giovane Spider-Man protagonista dello Spider-Verse.",

        "Shameik Moore",

        spiderverse,

        ["into_spiderverse", "across_spiderverse"],

        powers="Super forza, agilità, senso di ragno, invisibilità e bio-elettricità.",

        image="miles.jpg"

    )



    add_character(

        "Gwen Stacy",

        "Spider-Woman",

        "Spider-Woman proveniente da Terra-65.",

        "Hailee Steinfeld",

        spiderverse,

        ["into_spiderverse", "across_spiderverse"],

        gender="Female",

        powers="Super forza, agilità, senso di ragno e ragnatele.",

        image="spiderwoman.jpg"

    )



    add_character(

        "Peter B. Parker",

        "Spider-Man",

        "Versione più adulta e disillusa di Peter Parker che diventa mentore di Miles.",

        "Jake Johnson",

        spiderverse,

        ["into_spiderverse", "across_spiderverse"],

        powers="Super forza, agilità, senso di ragno, arrampicata e ragnatele."

    )



    add_character(

        "Peter Parker",

        "Spider-Man",

        "Spider-Man originale dell'universo di Miles Morales.",

        "Chris Pine",

        spiderverse,

        ["into_spiderverse"],

        status="Deceased",

        powers="Super forza, agilità, senso di ragno e ragnatele."

    )



    add_character(

        "Miguel O'Hara",

        "Spider-Man 2099",

        "Spider-Man proveniente dal futuro e leader della Spider-Society.",

        "Oscar Isaac",

        spiderverse,

        ["into_spiderverse", "across_spiderverse"],

        role="Antihero",

        powers="Super forza, artigli, zanne, agilità e tecnologia dimensionale.",

        image="miguel.jpeg"

    )



    add_character(

        "Jessica Drew",

        "Spider-Woman",

        "Spider-Woman e membro importante della Spider-Society.",

        "Issa Rae",

        spiderverse,

        ["across_spiderverse"],

        gender="Female",

        powers="Super forza, agilità, senso di ragno e abilità di combattimento."

    )



    add_character(

        "Hobie Brown",

        "Spider-Punk",

        "Spider-Man punk proveniente da un universo alternativo.",

        "Daniel Kaluuya",

        spiderverse,

        ["across_spiderverse"],

        powers="Super forza, agilità, senso di ragno e ragnatele."

    )



    add_character(

        "Pavitr Prabhakar",

        "Spider-Man India",

        "Spider-Man proveniente da Mumbattan.",

        "Karan Soni",

        spiderverse,

        ["across_spiderverse"],

        powers="Super forza, agilità, senso di ragno e ragnatele."

    )



    add_character(

        "Peni Parker",

        "SP//dr",

        "Giovane pilota di un robot collegato telepaticamente a un ragno.",

        "Kimiko Glenn",

        spiderverse,

        ["into_spiderverse", "across_spiderverse"],

        gender="Female",

        powers="Connessione telepatica con SP//dr e tecnologia avanzata."

    )



    add_character(

        "Peter Porker",

        "Spider-Ham",

        "Versione antropomorfa di Spider-Man proveniente da un universo cartoon.",

        "John Mulaney",

        spiderverse,

        ["into_spiderverse", "across_spiderverse"],

        character_type="Anthropomorphic Pig",

        powers="Super forza, agilità, senso di ragno e capacità cartoon."

    )



    add_character(

        "Peter Parker",

        "Spider-Man Noir",

        "Spider-Man proveniente da un universo noir ambientato negli anni Trenta.",

        "Nicolas Cage",

        spiderverse,

        ["into_spiderverse"],

        powers="Super forza, agilità, senso di ragno e combattimento."

    )



    add_character(

        "Jefferson Davis",

        "Jeff Morales",

        "Padre di Miles Morales e agente di polizia.",

        "Brian Tyree Henry",

        spiderverse,

        ["into_spiderverse", "across_spiderverse"],

        role="Supporting"

    )



    add_character(

        "Rio Morales",

        "Rio",

        "Madre di Miles Morales.",

        "Luna Lauren Vélez",

        spiderverse,

        ["into_spiderverse", "across_spiderverse"],

        role="Supporting",

        gender="Female"

    )



    add_character(

        "Aaron Davis",

        "Prowler",

        "Zio di Miles Morales e criminale che lavora per Kingpin.",

        "Mahershala Ali",

        spiderverse,

        ["into_spiderverse"],

        role="Villain",

        status="Deceased",

        powers="Tuta tecnologica, artigli e abilità di combattimento."

    )



    add_character(

        "Wilson Fisk",

        "Kingpin",

        "Potente criminale responsabile del collider dimensionale.",

        "Liev Schreiber",

        spiderverse,

        ["into_spiderverse"],

        role="Villain",

        powers="Forza fisica eccezionale e grande influenza criminale."

    )



    add_character(

        "Olivia Octavius",

        "Doctor Octopus",

        "Scienziata della Alchemax che lavora per Kingpin.",

        "Kathryn Hahn",

        spiderverse,

        ["into_spiderverse"],

        role="Villain",

        gender="Female",

        powers="Tentacoli meccanici e grande intelligenza scientifica."

    )



    add_character(

        "Norman Osborn",

        "Green Goblin",

        "Green Goblin dell'universo animato di Miles.",

        "Jorma Taccone",

        spiderverse,

        ["into_spiderverse"],

        role="Villain",

        status="Deceased",

        powers="Forza sovrumana, volo e trasformazione mostruosa."

    )



    add_character(

        "Tombstone",

        "Tombstone",

        "Uno degli uomini di fiducia di Kingpin.",

        "Marvin Jones III",

        spiderverse,

        ["into_spiderverse"],

        role="Villain",

        powers="Forza e resistenza sovrumane."

    )



    add_character(

        "Jonathan Ohnn",

        "The Spot",

        "Scienziato trasformato in un essere capace di creare portali dimensionali.",

        "Jason Schwartzman",

        spiderverse,

        ["across_spiderverse"],

        role="Villain",

        powers="Creazione e manipolazione di portali dimensionali."

    )



    add_character(

        "Ben Reilly",

        "Scarlet Spider",

        "Clone di Peter Parker e membro della Spider-Society.",

        "Andy Samberg",

        spiderverse,

        ["across_spiderverse"],

        powers="Super forza, agilità, senso di ragno e ragnatele."

    )



    add_character(

        "Margo Kess",

        "Spider-Byte",

        "Spider-Woman proveniente da una realtà digitale.",

        "Amandla Stenberg",

        spiderverse,

        ["across_spiderverse"],

        gender="Female",

        powers="Tecnologia digitale, avatar virtuale e abilità da Spider-Person."

    )



    add_character(

        "Lyla",

        "LYLA",

        "Assistente artificiale di Miguel O'Hara.",

        "Greta Lee",

        spiderverse,

        ["across_spiderverse"],

        role="Supporting",

        gender="Female",

        character_type="Artificial Intelligence",

        powers="Analisi dati, comunicazione e gestione tecnologica."

    )



    add_character(

        "George Stacy",

        "Captain Stacy",

        "Padre di Gwen Stacy e capitano della polizia.",

        "Shea Whigham",

        spiderverse,

        ["across_spiderverse"],

        role="Supporting"

    )



    # Universo alternativo visto alla fine di Across the Spider-Verse



    add_character(

        "Miles G. Morales",

        "Prowler",

        "Versione alternativa di Miles Morales proveniente da Terra-42.",

        "Jharrel Jerome",

        spiderverse,

        ["across_spiderverse"],

        role="Antihero",

        powers="Tecnologia Prowler e abilità di combattimento."

    )



    # ============================================================

    # SALVATAGGIO DATABASE

    # ============================================================



    db.session.commit()



    # ============================================================

    # RISULTATO

    # ============================================================



    print("=" * 60)

    print("DATABASE SPIDERVERSE CREATO CORRETTAMENTE")

    print("=" * 60)



    print(f"Universi: {Universe.query.count()}")

    print(f"Film: {Movie.query.count()}")

    print(f"Personaggi: {Character.query.count()}")



    print("=" * 60)



    for universe in Universe.query.all():

        print(f"\n{universe.name}")



        universe_movies = Movie.query.filter_by(

            universe_id=universe.id

        ).all()



        for movie in universe_movies:

            print(

                f"  - {movie.title} ({movie.year}): "

                f"{len(movie.characters)} personaggi"

            )



    print("=" * 60)
