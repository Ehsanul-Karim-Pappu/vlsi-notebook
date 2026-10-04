"""The 25-minute core path: which slides it keeps, and a shorter script for each.

    python build.py --core           also builds build/deck/core.html, the core deck

The full deck has about 11,000 words of notes, an hour and more of talk. The core keeps 69 of its
slides and the five labs, with about 2,800 spoken words: some 19 minutes at 150 words a minute,
plus about 3 minutes working the labs and 2 for transitions. Rehearse it and adjust. What it leaves out (the derivations, the patents'
details, latch-up, negative capacitance, Landauer, the CFET's two routes) stays in the full deck,
which is the extended route.

Each kept slide is (index in its scene, the start of its full English notes, English, Bangla).
build.py checks every index against that start, so a slide that moves can't silently pick up the
wrong script. The time budget, beat by beat, is in PLAN.md.
"""

CORE = {
    "Ch00ColdOpen": [
        (0, "In December 1947, the first working",
         "In December 1947 the first working transistor sat on a lab bench at Bell Labs. By 2018, by one "
         "estimate, we had made about thirteen sextillion of them: a thirteen with twenty-one zeros. "
         "That's more than any other thing people have ever made.",
         "1947-এর December-এ প্রথম চালু transistor-টা Bell Labs-এর একটা bench-এ বসা ছিল। একটা হিসাবে, 2018-এর মধ্যে আমরা "
         "এর প্রায় তেরো sextillion বানায়ে ফেলছি: তেরোর পরে একুশটা শূন্য। মানুষের বানানো আর কোনো জিনিস এত বানানো হয় নাই।"),
        (3, "Zoom in, and the chip is a city",
         "Here's where they are today. This is Apple's A20 Pro, from the iPhone 18 Pro, made by TSMC on "
         "its 2 nanometre process, the first iPhone chip with gate-all-around transistors. Zoom into a "
         "core and you reach the view you work in every day: rows of standard cells, poly crossing "
         "diffusion.",
         "আজকে এগুলা কোথায়, দেখেন। এইটা Apple-এর A20 Pro, iPhone 18 Pro-র chip, TSMC ওদের 2 nanometre process-এ বানায়, "
         "gate-all-around transistor সহ প্রথম iPhone chip। একটা core-এ zoom করেন, পৌঁছে যাবেন রোজকার চেনা view-তে: standard "
         "cell-এর সারি, diffusion-এর উপর দিয়া poly।"),
        (6, "Here is what such a transistor looks",
         "And here's one transistor in 3D. It's an illustrative nanosheet model from FET Lab, not the "
         "measured chip. Three sheets of silicon, five nanometres thick, carry the current from source to "
         "drain, and the gate wraps all the way around every one of them.",
         "আর এই যে একটা transistor, 3D-তে। এইটা FET Lab-এর একটা illustrative nanosheet model, মাপা chip না। পাঁচ nanometre "
         "পুরু তিনটা silicon sheet source থেকে drain-এ current নেয়, আর gate প্রত্যেকটার চারপাশ পুরা ঘিরে থাকে।"),
        (9, "Every one of them has one job",
         "Every one of them has one job: let current through, or stop it. On, off. This talk is about how "
         "we got from the first one to this one, and why, every time we made it smaller, stopping the "
         "current turned out to be the hard part.",
         "এদের প্রত্যেকটার একটাই কাজ: current যাইতে দেওয়া, নয়তো থামানো। On, off। এই talk হইলো প্রথমটা থেকে এইটা পর্যন্ত কীভাবে "
         "আসলাম, আর প্রত্যেকবার ছোট করার সময় current থামানোটাই কেন কঠিন অংশ হয়ে দাঁড়াইছে, সেই নিয়া।"),
        (16, "Five shapes: three in sixty years",
         "Five shapes: the planar transistor, the FinFET, the nanosheet, and two on the roadmap, the "
         "forksheet and the CFET. Each one answered a problem, of physics or of packing. Let's see why "
         "each had to happen.",
         "পাঁচটা আকার: planar transistor, FinFET, nanosheet, আর roadmap-এ দুইটা, forksheet আর CFET। প্রত্যেকটা একটা সমস্যার "
         "উত্তর, physics-এর বা জায়গার। চলেন দেখি প্রত্যেকটা কেন আসতে হইছে।"),
    ],
    "Ch01BeforeTheSwitch": [
        (0, "Before we get to that 1925 patent",
         "First, what the transistor replaced.",
         "প্রথমে দেখি, transistor কী সরাইছে।"),
        (4, "About eighteen thousand tubes",
         "Before transistors, the switch was the vacuum tube: a hot cathode boiling off electrons, a grid "
         "that lets them through or turns them back, a plate that collects them. ENIAC, in 1946, used "
         "about eighteen thousand of them and some 150 kilowatts, and tubes kept burning out. Everyone "
         "wanted a cold, solid switch.",
         "Transistor-এর আগে switch ছিল vacuum tube: একটা গরম cathode থেকে electron বের হয়, একটা grid ওদের যাইতে দেয় বা ফিরায়ে "
         "দেয়, একটা plate ওদের ধরে। 1946-এ ENIAC এর প্রায় আঠারো হাজারটা ব্যবহার করত, প্রায় 150 kilowatt খরচ করে, আর tube একটার পর "
         "একটা পুড়ত। সবাই চাইত একটা ঠান্ডা, solid switch।"),
        (5, "To see why ENIAC still needed tubes",
         "And the idea already existed. In 1925 Julius Lilienfeld patented a field-effect device: a metal "
         "plate over a thin film of semiconductor, insulated from it. Put a voltage on the plate, and it "
         "should pull charge into the film and change the current through it. That's a MOSFET, in "
         "everything but name.",
         "আর idea-টা আগেই ছিল। 1925-এ Julius Lilienfeld একটা field-effect device patent করেন: পাতলা semiconductor film-এর উপর "
         "একটা metal plate, মাঝে insulation। Plate-এ voltage দিলে এইটা film-এ charge টেনে আনবে আর ভিতরের current বদলাবে। নামে না "
         "হলেও, এইটা একটা MOSFET।"),
        (7, "On paper, the effect is big",
         "On paper, the effect is big: the plate and the film are a capacitor, and ten volts should pull "
         "in plenty of charge. In practice, when Shockley tried it at Bell Labs in 1945, almost nothing "
         "happened.",
         "কাগজে effect-টা বড়: plate আর film মিলে একটা capacitor, আর দশ volt অনেক charge টেনে আনার কথা। বাস্তবে, 1945-এ Bell "
         "Labs-এ Shockley যখন চেষ্টা করেন, প্রায় কিছুই হয় নাই।"),
        (8, "At Bell Labs in 1945",
         "John Bardeen worked out why: the surface. Where the crystal ends, there are broken bonds, "
         "states that trap the charge the gate induces before it can reach the semiconductor. In our "
         "simple model, with a bare surface only about 2 percent of that charge ends up in the "
         "semiconductor. The rest is stuck at the surface.",
         "John Bardeen বের করেন কেন: surface। Crystal যেখানে শেষ, সেখানে ভাঙা bond থাকে, এমন state যেগুলা gate-এর আনা charge "
         "semiconductor-এ পৌঁছানোর আগেই আটকায়ে ফেলে। আমাদের সহজ model-এ, খালি surface থাকলে ওই charge-এর মাত্র প্রায় 2 percent "
         "semiconductor-এ যায়। বাকিটা surface-এ আটকে থাকে।"),
        (12, "That was the dead end of the 1940s",
         "That was the dead end of the 1940s. So Bardeen and Brattain stopped fighting the surface, and "
         "started poking it.",
         "এইটাই ছিল 1940-এর দশকের কানা গলি। তাই Bardeen আর Brattain surface-এর সাথে লড়াই থামায়ে ওইটারে খোঁচাইতে শুরু করেন।"),
    ],
    "Ch02AccidentalTransistor": [
        (0, "Bell Labs, December 1947",
         "December 1947. They were looking for amplification, on purpose.",
         "1947-এর December। ওরা ইচ্ছা করেই amplification খুঁজতেছিলেন।"),
        (1, "This is a replica of the first",
         "On the 16th of December it worked: two gold contacts pressed onto germanium, a hair's breadth "
         "apart, and the output was a bigger copy of the input. Not the field effect they were after, an "
         "unexpected mechanism, but real amplification. This is a replica of that first transistor, and "
         "its patent drawing.",
         "16 December-এ এইটা কাজ করে: germanium-এর উপর চুলের মতো সরু ফাঁকে দুইটা gold contact, আর output হইলো input-এর বড় একটা "
         "copy। ওরা যে field effect খুঁজতেছিলেন সেইটা না, একটা অপ্রত্যাশিত mechanism, কিন্তু আসল amplification। এইটা ওই প্রথম "
         "transistor-এর একটা replica, আর তার patent drawing।"),
        (5, "Because the electrons have to get over",
         "Shockley's junction transistor followed in 1948. Electrons climb a hill to cross from emitter to "
         "collector, so the current is exponential in the base voltage: about 60 millivolts for ten times "
         "the current. Remember that 60. It comes back.",
         "1948-এ আসে Shockley-র junction transistor। Emitter থেকে collector-এ যাইতে electron-রে একটা hill বাইতে হয়, তাই current "
         "base voltage-এর সাথে exponential: প্রায় 60 millivolt-এ দশ গুণ current। এই 60 মনে রাখেন। এইটা আবার আসবে।"),
        (7, "But as a building block for logic",
         "But as a logic switch, a bipolar transistor needs base current just to stay on, so a chip full "
         "of them burns power standing still. The field effect needs almost no input current. It was still "
         "the better idea, if only the surface could be fixed.",
         "কিন্তু logic switch হিসাবে bipolar transistor-এর শুধু on থাকতেই base current লাগে, তাই এগুলায় ভরা chip বসে থেকেও power "
         "খায়। Field effect-এর input current প্রায় লাগেই না। ওইটাই তখনও ভালো idea ছিল, যদি শুধু surface ঠিক করা যাইত।"),
    ],
    "Ch03Glass": [
        (0, "So the field effect was stuck",
         "The fix came from glass.",
         "সমাধান আসে glass থেকে।"),
        (1, "In the mid-1950s at Bell Labs",
         "In the mid-1950s at Bell Labs, Carl Frosch and Lincoln Derick found that silicon grows its own "
         "glass, silicon dioxide, and that it blocks dopants. Open a window in it and you dope only there. "
         "Every mask layer you draw still works this way: open where you drew, blocked elsewhere.",
         "1950-এর দশকের মাঝামাঝি Bell Labs-এ Carl Frosch আর Lincoln Derick দেখেন silicon নিজের glass, silicon dioxide, grow করে, "
         "আর ওইটা dopant আটকায়। এতে একটা জানালা খোলেন, শুধু ওইখানে dope হয়। আপনি যত mask layer আঁকেন, সব এখনো এভাবেই কাজ করে: "
         "যেখানে আঁকছেন সেখানে খোলা, বাকি জায়গা বন্ধ।"),
        (2, "Then Mohamed Atalla at Bell Labs",
         "Then Mohamed Atalla found something even more important: a carefully grown oxide also heals the "
         "surface. It ties up the broken bonds. In our model, the semiconductor's share of the charge goes "
         "from about 2 percent to about 96. The gate can finally reach the silicon.",
         "তারপর Mohamed Atalla আরও বড় একটা জিনিস পান: যত্ন করে grow করা oxide surface-ও সারায়ে দেয়। ভাঙা bond-গুলা বেঁধে ফেলে। আমাদের "
         "model-এ semiconductor-এর charge-এর ভাগ প্রায় 2 percent থেকে প্রায় 96-এ ওঠে। Gate শেষ পর্যন্ত silicon-এর নাগাল পায়।"),
        (3, "With the surface tamed",
         "With the surface tamed, it all arrives at once: Kilby's integrated circuit in 1958, the planar "
         "process and Noyce's planar chip in 1959, and in 1959 to 60, Atalla and Kahng's MOSFET: metal, "
         "oxide, semiconductor.",
         "Surface বশে আসার পর সব একসাথে আসে: 1958-এ Kilby-র integrated circuit, 1959-এ planar process আর Noyce-এর planar chip, আর "
         "1959 থেকে 60-এ Atalla আর Kahng-এর MOSFET: metal, oxide, semiconductor।"),
        (5, "So how does a gate make a channel",
         "So how does a gate make a channel? Kahng's device was p-channel; we'll draw the n-channel mirror "
         "image, on p-type silicon. Raise the gate voltage and the bands bend down at the surface. Past the "
         "threshold, the surface fills with electrons: an inverted layer, joining source to drain. That's "
         "the channel.",
         "তাহলে gate কীভাবে channel বানায়? Kahng-এর device ছিল p-channel; আমরা আঁকব তার n-channel আয়নার ছবি, p-type silicon-এর উপর। "
         "Gate voltage বাড়ান, surface-এ band নিচে বাঁকে। Threshold পার হলে surface electron-এ ভরে যায়: একটা উল্টানো layer, source আর "
         "drain-রে জোড়া দেয়। এইটাই channel।"),
        (7, "Now the current. Look at a transistor",
         "And the current is set by what you draw. In saturation, the square law: I-D goes as W over L, "
         "times the overdrive squared. The ratio you draw sets the current, which is why matched devices "
         "copy W, L, fingers and orientation.",
         "আর current ঠিক হয় আপনি যা আঁকেন তা দিয়া। Saturation-এ square law: I-D চলে W বাই L গুণ overdrive-এর square হারে। আপনার আঁকা "
         "ratio current ঠিক করে, এই কারণেই matched device-গুলা W, L, finger আর orientation একই রাখে।"),
        (15, "Here's how it switches",
         "In 1963 Frank Wanlass paired an n and a p transistor: CMOS. With the input at either rail, one of "
         "them is off, so ideally no current flows from supply to ground, apart from leakage. Only while the "
         "input passes through the middle do both conduct, briefly. Most of the power goes into charging "
         "the load: alpha C V squared f.",
         "1963-এ Frank Wanlass একটা n আর একটা p transistor জোড়া দেন: CMOS। Input যেকোনো rail-এ থাকলে একটা off, তাই আদর্শভাবে supply "
         "থেকে ground-এ current যায় না, leakage বাদে। শুধু input মাঝখান দিয়া যাওয়ার সময় দুইটাই অল্প সময় চলে। বেশিরভাগ power যায় load "
         "charge করতে: alpha C V square f।"),
        (18, "So by the mid-1960s we have it",
         "So by the mid-1960s we have it: a switch that barely leaks, spends power mostly when it switches, "
         "and is made by the billion with masks and glass. So what happens if you draw everything smaller?",
         "তো 1960-এর দশকের মাঝামাঝি আমাদের হাতে চলে আসলো: এমন switch যেটা প্রায় leak করে না, power খরচ করে মূলত switch করার সময়, আর "
         "mask আর glass দিয়া billion-এ বানানো যায়। তাহলে সব ছোট করে আঁকলে কী হয়?"),
    ],
    "Ch04FreeLunch": [
        (0, "For the next forty years",
         "For the next forty years, the answer was: everything gets better.",
         "পরের চল্লিশ বছর উত্তর ছিল: সবকিছু ভালো হয়।"),
        (1, "In 1965 Gordon Moore",
         "In 1965 Gordon Moore plotted the number of components per chip and saw it doubling every year. "
         "In 1975 he revised it to every two years. It isn't a law of physics. It's economics: the count "
         "at which each component is cheapest.",
         "1965-এ Gordon Moore chip-প্রতি component-এর সংখ্যা plot করে দেখেন প্রতি বছর দ্বিগুণ হইতেছে। 1975-এ বদলায়ে বলেন প্রতি দুই বছরে। "
         "এইটা physics-এর নিয়ম না। এইটা economics: কত component-এ প্রত্যেকটা সবচেয়ে সস্তা।"),
        (2, "Now take Moore's 1975 version",
         "Start that two-year doubling from Intel's first microprocessor, the 4004 in 1971, with 2,300 "
         "transistors. Our extrapolation lands near today's largest chips, like NVIDIA's B200: two dies, "
         "208 billion transistors. Fifty years on one line.",
         "ওই দুই বছরে দ্বিগুণ শুরু করেন Intel-এর প্রথম microprocessor থেকে, 1971-এর 4004, 2,300 transistor। আমাদের extrapolation আজকের "
         "সবচেয়ে বড় chip-এর কাছে পৌঁছায়, যেমন NVIDIA-র B200: দুইটা die, 208 billion transistor। পঞ্চাশ বছর এক লাইনে।"),
        (4, "His recipe: shrink every dimension",
         "In 1974 Robert Dennard and his colleagues at IBM said how to do it. Shrink every dimension by a "
         "factor kappa: length, width, oxide. Shrink the voltage by kappa too. Then the electric fields "
         "inside stay the same, and the transistor behaves the same, only smaller.",
         "1974-এ IBM-এ Robert Dennard আর তাঁর সহকর্মীরা বলেন কীভাবে। প্রত্যেকটা মাপ kappa দিয়া ছোট করেন: length, width, oxide। Voltage-ও "
         "kappa দিয়া। তাহলে ভিতরের electric field একই থাকে, আর transistor একই রকম আচরণ করে, শুধু ছোট।"),
        (5, "Here's what that meant, generation",
         "Then every generation gives you twice the transistors in the same area, each one faster, and the "
         "same heat per square millimetre. That was the free lunch, and it's why your phone has billions of "
         "transistors and doesn't melt.",
         "তাহলে প্রত্যেক generation-এ একই area-তে দ্বিগুণ transistor, প্রত্যেকটা আরও দ্রুত, আর প্রতি square millimetre-এ একই heat। এইটাই "
         "ছিল free lunch, আর এই কারণেই আপনার phone-এ billion billion transistor থাকে, তবু গলে না।"),
        (8, "But look at Dennard's table again",
         "But look at Dennard's table again. Every row could keep shrinking for as long as we could draw "
         "smaller, except one: the voltage. Try it in the lab.",
         "কিন্তু Dennard-এর table-টা আবার দেখেন। যতদিন ছোট আঁকা যায়, প্রত্যেকটা row ছোট হইতে পারে, একটা বাদে: voltage। Lab-এ try করেন।"),
    ],
    "Ch05Boltzmann": [
        (0, "For forty years, shrinking worked",
         "Around 2005 something stopped. A big part of the reason isn't engineering. It's thermodynamics.",
         "2005-এর দিকে একটা জিনিস থেমে গেল। কারণের বড় অংশ engineering না। সেইটা thermodynamics।"),
        (1, "Remember the hill from the junction",
         "Remember the hill from the junction transistor? Here it is for the MOSFET: electrons waiting in the "
         "source, and a barrier between them and the drain whose height the gate sets. The current is the "
         "electrons that get over.",
         "Junction transistor-এর hill মনে আছে? এই যে MOSFET-এর জন্য: source-এ electron অপেক্ষা করতেছে, আর ওদের আর drain-এর মাঝে একটা "
         "barrier, যার উচ্চতা gate ঠিক করে। Current হইলো যে electron-গুলা পার হয়।"),
        (4, "Here's the question that matters",
         "Here's the question that matters: when the switch is off, how many still get over? Those are your "
         "leakage. The electrons' energies have a Boltzmann tail, and the share above the barrier falls as e "
         "to the minus E over k-T. Temperature sets it, not the designer.",
         "আসল প্রশ্ন এইটা: switch off থাকলে কতগুলা তবুও পার হয়? ওইগুলাই আপনার leakage। Electron-দের energy-র একটা Boltzmann tail আছে, "
         "আর barrier-এর উপরের ভাগ কমে e to the minus E over k-T হারে। এইটা temperature ঠিক করে, designer না।"),
        (6, "So how far do we have to lower",
         "So to get ten times as many over, you lower the barrier by k-T times ln 10: about 60 "
         "milli-electron-volts at room temperature. Another 60, a hundred times. Every 60 is one decade of "
         "current.",
         "তাই দশ গুণ বেশি পার করাইতে barrier নামাইতে হয় k-T গুণ ln 10: room temperature-এ প্রায় 60 milli-electron-volt। আরও 60, একশ গুণ। "
         "প্রতি 60 মানে current-এর এক decade।"),
        (14, "Put the two pieces together",
         "One more piece: the gate pushes on the channel through the oxide, a capacitive divider, so the "
         "channel moves by only one over m of the gate voltage. Together: the subthreshold swing. At room "
         "temperature an ordinary transistor needs at least 60 millivolts of gate for each decade of "
         "current.",
         "আরও একটা অংশ: gate oxide-এর ভিতর দিয়া channel-রে ঠেলে, একটা capacitive divider, তাই channel gate voltage-এর মাত্র এক বাই m নড়ে। "
         "একসাথে: subthreshold swing। Room temperature-এ একটা সাধারণ transistor-এর current-এর প্রতি decade-এর জন্য gate-এ অন্তত 60 "
         "millivolt লাগে।"),
        (18, "And here's the trap",
         "And here's the trap. To lower the supply and keep the on-current, you must lower the threshold, "
         "and every 70 millivolts or so off the threshold costs about ten times the leakage. Do that a few "
         "times and the off current is no longer off. So the supply voltage stopped falling, near one volt.",
         "আর এইখানে ফাঁদ। Supply কমায়ে on-current রাখতে হলে threshold কমাইতে হয়, আর threshold থেকে প্রতি প্রায় 70 millivolt-এর দাম প্রায় দশ "
         "গুণ leakage। কয়েকবার করলে off current আর off থাকে না। তাই supply voltage এক volt-এর কাছে এসে কমা থামায়ে দিল।"),
        (19, "You can see it in the clock speed",
         "You can see it in the clock speed. Base clocks rose about a thousandfold, then around 2004 levelled "
         "off at three to four gigahertz. With the voltage stuck, a faster clock means more heat. Chips got "
         "more cores instead.",
         "Clock speed-এ এইটা দেখা যায়। Base clock প্রায় হাজার গুণ বাড়ছে, তারপর 2004-এর দিকে তিন থেকে চার gigahertz-এ থেমে গেছে। Voltage "
         "আটকে থাকলে clock বাড়ানো মানে বেশি heat। তার বদলে chip-এ বেশি core আসছে।"),
        (22, "The fix was a new material",
         "There was a second wall at the same time. The gate oxide was down to about 1.2 nanometres, a few "
         "atoms, and electrons tunnelled straight through it. The fix was hafnium oxide: a higher k, so a "
         "thicker layer gives the same grip with far less tunnelling. Intel shipped it in 2007.",
         "একই সময়ে আরেকটা দেয়াল ছিল। Gate oxide নামছিল প্রায় 1.2 nanometre-এ, কয়েকটা atom, আর electron সোজা এর ভিতর দিয়া tunnel করতেছিল। "
         "সমাধান hafnium oxide: k বেশি, তাই মোটা layer-ও একই grip দেয়, অনেক কম tunnelling-এ। Intel 2007-এ ship করে।"),
        (23, "So that's the state of things",
         "So by the mid-2000s we had fixed the oxide. We could not fix Boltzmann. Try it in the lab.",
         "তো 2000-এর দশকের মাঝামাঝি আমরা oxide ঠিক করছি। Boltzmann-রে ঠিক করতে পারি নাই। Lab-এ try করেন।"),
    ],
    "Ch06LosingGrip": [
        (0, "Short-channel effects had been fought",
         "Then the channel got short enough for the drain to join in.",
         "তারপর channel এত ছোট হইলো যে drain-ও খেলায় ঢুকে পড়ল।"),
        (1, "Here's the hill again, now drawn",
         "Here's the hill again, drawn along the transistor: source on the left, drain on the right, gate on "
         "top. In a long channel the gate holds the top of the hill. Put a voltage on the drain and the drain "
         "end drops, but the top doesn't move. The gate is in charge.",
         "এই যে hill আবার, এবার transistor বরাবর আঁকা: বামে source, ডানে drain, উপরে gate। লম্বা channel-এ gate hill-এর চূড়া ধরে রাখে। Drain-এ "
         "voltage দেন, drain-এর দিকটা নামে, কিন্তু চূড়া নড়ে না। Gate-এর হাতেই control।"),
        (3, "Now shrink the channel",
         "Now shorten the channel. The source and the drain each bend the potential near them, and when they "
         "get close, their bends meet and pull the hill down by themselves. That's threshold roll-off.",
         "এবার channel ছোট করেন। Source আর drain প্রত্যেকে নিজের কাছের potential বাঁকায়, আর কাছাকাছি আসলে বাঁকগুলা মিলে যায় আর নিজেরাই hill "
         "টেনে নামায়। এইটা threshold roll-off।"),
        (4, "And now the drain voltage",
         "And on a short channel the drain voltage lowers the top of the barrier too. That's DIBL, "
         "drain-induced barrier lowering. The drain has become a second gate, one you don't control, and the "
         "leakage climbs.",
         "আর ছোট channel-এ drain voltage-ও barrier-এর চূড়া নামায়। এইটা DIBL, drain-induced barrier lowering। Drain হয়ে গেছে দ্বিতীয় একটা gate, "
         "যেটা আপনার control-এ নাই, আর leakage বাড়ে।"),
        (5, "Why does this happen",
         "The reason is a length, lambda: how far the source's and the drain's influence reaches into the "
         "channel. In our toy model it depends on the channel's thickness, the oxide, and how many sides the "
         "gate holds. Long compared with lambda, the gate wins. Short, the drain wins. It all depends on L "
         "over lambda.",
         "কারণ একটা দৈর্ঘ্য, lambda: source আর drain-এর প্রভাব channel-এর কত ভিতরে পৌঁছায়। আমাদের toy model-এ এইটা নির্ভর করে channel-এর "
         "thickness, oxide, আর gate কয় দিক ধরে তার উপর। Lambda-র তুলনায় লম্বা হলে gate জেতে। ছোট হলে drain জেতে। সব L বাই lambda-র উপর।"),
        (13, "For analog, DIBL has a direct price",
         "For analog, this has a direct price. If the drain moves the barrier, the drain voltage moves the "
         "current, so the output resistance falls, and with it the intrinsic gain, g-m r-o. That's one reason "
         "analog transistors are drawn longer than minimum.",
         "Analog-এর জন্য এর সরাসরি দাম আছে। Drain যদি barrier নাড়ায়, drain voltage current নাড়ায়, তাই output resistance কমে, আর সাথে intrinsic "
         "gain, g-m r-o। Analog transistor minimum-এর চেয়ে লম্বা আঁকার এইটা একটা কারণ।"),
        (14, "So how do you get the grip back",
         "So how do you get the grip back? Not by pushing the gate harder. Make lambda smaller: a thinner "
         "channel, and gate on more than one side. Try it in the lab.",
         "তাহলে grip ফেরত পাবেন কীভাবে? Gate-এ আরও জোরে চাপ দিয়া না। Lambda ছোট করেন: পাতলা channel, আর একাধিক দিকে gate। Lab-এ try "
         "করেন।"),
    ],
    "Ch07FinFET": [
        (0, "If you can't put a gate underneath",
         "If you can't put a gate under a flat channel, stand the channel up.",
         "সমতল channel-এর নিচে gate বসাইতে না পারলে, channel-রে দাঁড় করান।"),
        (1, "1989: at Hitachi",
         "That's the fin: a thin wall of silicon standing on the wafer, gated from the sides. Hitachi showed "
         "one, DELTA, in 1989. Berkeley's FinFET came in 1998 and 99. And in 2011 Intel announced its 22 "
         "nanometre tri-gate transistors, in products the next year.",
         "এইটাই fin: wafer-এর উপর দাঁড়ানো silicon-এর একটা পাতলা দেয়াল, পাশ থেকে gate করা। 1989-এ Hitachi একটা দেখায়, DELTA। Berkeley-র "
         "FinFET আসে 1998 আর 99-এ। আর 2011-এ Intel ওদের 22 nanometre tri-gate transistor ঘোষণা করে, পরের বছর product-এ।"),
        (4, "Now cut it across, right through",
         "Cut it across, through the gate. The gate wraps over the top and down both sides of each fin: three "
         "faces instead of one. With a six nanometre fin, lambda drops to a couple of nanometres. The grip is "
         "back.",
         "এইটারে gate-এর ভিতর দিয়া আড়াআড়ি কাটেন। Gate প্রত্যেক fin-এর উপর দিয়া আর দুই পাশ দিয়া মুড়ে আছে: এক দিকের বদলে তিন দিক। ছয় "
         "nanometre fin-এ lambda নেমে আসে দুই-এক nanometre-এ। Grip ফিরে আসছে।"),
        (6, "So what's the width of a FinFET",
         "So what's its width? Current flows from source to drain along the fin, on both sidewalls and the "
         "top, so each fin counts twice its height plus its width. Two fins, 45 nanometres tall: 192 "
         "nanometres.",
         "তাহলে এর width কত? Current fin বরাবর source থেকে drain-এ যায়, দুই পাশের দেয়াল আর উপর দিয়া, তাই প্রত্যেক fin-এর হিসাব দুইগুণ height যোগ "
         "width। 45 nanometre উঁচু দুইটা fin: 192 nanometre।"),
        (7, "But there's a catch, and it changed",
         "But every fin is the same height, so the width comes in whole fins: 96, 192, 288 nanometres, nothing "
         "in between. In layout you no longer draw W; you pick a number of fins, and a one-to-two mirror is two "
         "fins and four.",
         "কিন্তু সব fin-এর height এক, তাই width আসে পুরা fin-এ: 96, 192, 288 nanometre, মাঝখানে কিছু না। Layout-এ আপনি আর W আঁকেন না; fin-এর "
         "সংখ্যা বাছেন, আর এক-দুই mirror মানে দুইটা fin আর চারটা।"),
        (11, "So here's the next idea",
         "And the fin ran out of room: it's hard to make thinner, or taller. So turn it on its side, and slice "
         "it into sheets.",
         "আর fin-এর জায়গা ফুরাইছে: আরও পাতলা বা লম্বা করা কঠিন। তাই এইটারে কাত করে শোয়ান, আর sheet-এ কাটেন।"),
    ],
    "Ch08Nanosheet": [
        (2, "Remember the nanosheet transistor",
         "That's the nanosheet we started with: sheets of silicon five nanometres thick, with the gate all "
         "the way around each one, four faces. Samsung started making them in 2022; TSMC's N2 and Intel's 18A "
         "followed in 2025.",
         "এইটাই শুরুর সেই nanosheet: পাঁচ nanometre পুরু silicon sheet, প্রত্যেকটার চারপাশ ঘিরে gate, চার দিক। Samsung 2022-এ বানানো শুরু করে; "
         "TSMC-র N2 আর Intel-এর 18A আসে 2025-এ।"),
        (4, "And here's the part layout people",
         "Each sheet counts all four faces, and here's the part layout people care about: the sheet width is "
         "set by the mask, not by a fin height. Width is something you draw again.",
         "প্রত্যেক sheet-এর চার দিকই হিসাবে আসে, আর layout-এর লোকদের আসল আগ্রহ এইখানে: sheet-এর width mask দিয়া ঠিক হয়, fin height দিয়া না। "
         "Width আবার এমন জিনিস যেটা আপনি আঁকেন।"),
        (5, "How do you put a gate under a sheet",
         "How do you put a gate under a sheet of silicon? You don't. You grow the space for it first: a stack "
         "of silicon and silicon-germanium, a few nanometres each. The silicon will be the channels. The "
         "silicon-germanium just holds the place.",
         "Silicon-এর sheet-এর নিচে gate বসান কীভাবে? বসান না। আগে জায়গাটা grow করেন: silicon আর silicon-germanium-এর stack, প্রত্যেকটা কয়েক "
         "nanometre। Silicon হবে channel। Silicon-germanium শুধু জায়গা ধরে রাখে।"),
        (8, "Now the magic. Pull out the dummy",
         "Then a dummy gate, inner spacers, and the source and drain grown from the sheets' ends, sitting on an "
         "insulator. Now the magic: pull out the dummy gate, dissolve the silicon-germanium, and the sheets "
         "hang in mid-air, held at their ends.",
         "তারপর একটা dummy gate, inner spacer, আর sheet-এর মাথা থেকে grow করা source আর drain, একটা insulator-এর উপর বসা। এবার জাদু: dummy "
         "gate তোলেন, silicon-germanium গলান, sheet-গুলা শূন্যে ঝুলে থাকে, দুই মাথায় ধরা।"),
        (9, "Finally, coat every exposed surface",
         "Coat everything with oxide and high-k, fill every gap with metal, and the gate wraps all the way "
         "around. That's one common route, and the idea at its heart: build the gate's space from a material "
         "you dissolve later.",
         "সবকিছুতে oxide আর high-k-এর আস্তর দেন, প্রত্যেকটা ফাঁক metal দিয়া ভরেন, gate পুরা চারপাশ ঘিরে ফেলে। এইটা একটা প্রচলিত পথ, আর এর মূল "
         "idea: gate-এর জায়গা এমন material দিয়া বানান যেটা পরে গলায়ে ফেলবেন।"),
        (11, "So what stops the nanosheet",
         "So what stops the nanosheet? Look at the cell's height, set by the number of metal tracks. And in it, "
         "the space between the n and the p sheets: here 46 nanometres, a third of the cell. It can't shrink "
         "much, because n and p need different gate metals, patterned apart.",
         "তাহলে nanosheet-রে আটকায় কে? Cell-এর height দেখেন, যেটা metal track-এর সংখ্যা দিয়া ঠিক হয়। আর তার ভিতরে n আর p sheet-এর মাঝের জায়গা: "
         "এইখানে 46 nanometre, cell-এর তিন ভাগের এক ভাগ। এইটা খুব একটা কমে না, কারণ n আর p-এর আলাদা gate metal লাগে, আলাদা করে pattern করা।"),
    ],
    "Ch09Forksheet": [
        (6, "And what does it buy",
         "One answer, on imec's roadmap: the forksheet. Put a thin insulating wall between n and p and push "
         "the sheets right against it. In these schematic models the cell gets about a fifth shorter. imec's "
         "2021 forksheets switched about as well as nanosheets, and the version on the roadmap puts the wall "
         "at the cell's edge.",
         "একটা উত্তর, imec-এর roadmap-এ: forksheet। n আর p-এর মাঝে একটা পাতলা insulating wall বসান আর sheet-গুলা ওইটার গায়ে ঠেলে দেন। এই "
         "schematic model-গুলায় cell প্রায় পাঁচ ভাগের এক ভাগ ছোট হয়। imec-এর 2021-এর forksheet প্রায় nanosheet-এর মতোই switch করছে, আর "
         "roadmap-এর version-টা wall বসায় cell-এর কিনারায়।"),
    ],
    "Ch10CFET": [
        (0, "Every transistor so far has been built",
         "Or remove the space completely, by building upward.",
         "নয়তো উপরের দিকে বানায়ে জায়গাটাই পুরা সরায়ে দেন।"),
        (4, "Cut across the gate. Two pink sheets",
         "The CFET, the complementary FET, stacks the n transistor right on top of the p. Cut across the gate: "
         "two sheets below, two above, one gate around all four in this model. Two transistors, one "
         "footprint. It's on imec's roadmap for the early 2030s.",
         "CFET, মানে complementary FET, n transistor-রে সোজা p-এর উপরে বসায়। Gate বরাবর কাটেন: নিচে দুইটা sheet, উপরে দুইটা, এই model-এ একটা "
         "gate চারটারেই ঘিরে। দুইটা transistor, একটার জায়গা। imec-এর roadmap-এ এইটা 2030-এর দশকের শুরুতে।"),
        (6, "Now line up the four inverter cells",
         "Line up the four inverter cells at one scale, rail to rail: 156, 136, 106 and 74 nanometres, in these "
         "schematic models. Each step took the n-to-p space away, and the cell got shorter.",
         "চারটা inverter cell একই scale-এ পাশাপাশি রাখেন, rail থেকে rail: এই schematic model-গুলায় 156, 136, 106 আর 74 nanometre। প্রত্যেক "
         "ধাপে n-to-p space সরানো হইছে, আর cell ছোট হইছে।"),
        (7, "Look at the CFET cell's rails",
         "Look where the CFET's power rails went: to the back of the wafer, where they can be thick, so less "
         "voltage is lost on the way. That doesn't wait for the CFET: Intel already ships backside power with "
         "nanosheets, in 18A.",
         "CFET-এর power rail কোথায় গেল দেখেন: wafer-এর পেছনে, যেখানে মোটা হইতে পারে, তাই পথে কম voltage হারায়। এইটার জন্য CFET-এর অপেক্ষা "
         "লাগে না: Intel nanosheet-এর সাথেই backside power ship করতেছে, 18A-তে।"),
        (8, "And there's heat",
         "And stacking stacks the heat: up to twice the power per area, depending on the workload. With the heat "
         "sink below the wafer, the upper tier's heat has the longer way out. Now build a cell yourself.",
         "আর stack করলে heat-ও stack হয়: area-প্রতি দুইগুণ পর্যন্ত power, workload-এর উপর নির্ভর করে। Heat sink wafer-এর নিচে থাকলে উপরের "
         "tier-এর heat-এর বের হওয়ার পথ লম্বা। এবার নিজে একটা cell বানান।"),
    ],
    "Ch11Beyond": [
        (0, "Everything from here on is research",
         "From here on, it's research.",
         "এখান থেকে সব research।"),
        (2, "So use a material that is thin",
         "Research now: channels just a few atoms thick, like molybdenum disulfide, with no surface to roughen. "
         "imec's roadmap brings them in around the 2040s. And their catch is the contacts, where Bardeen's old "
         "surface states come back.",
         "এখনকার research: মাত্র কয়েকটা atom পুরু channel, যেমন molybdenum disulfide, যার surface-এ খাঁজ নাই। imec-এর roadmap এগুলারে আনে "
         "2040-এর দশকের আশেপাশে। আর এদের ঝামেলা contact-এ, যেখানে Bardeen-এর পুরানো surface state ফিরে আসে।"),
        (5, "The tunnel FET",
         "And switches that try to beat 60 millivolts per decade, by tunnelling through the barrier instead of "
         "climbing over it. Tunnel transistors have done it in the lab, and in 2024 an MIT team did it while "
         "still carrying useful current.",
         "আর এমন switch যেগুলা 60 millivolt প্রতি decade-রে হারাইতে চায়, barrier বাইয়া না উঠে ভেদ করে tunnel করে। Tunnel transistor lab-এ এইটা "
         "করছে, আর 2024-এ MIT-এর একটা team কাজের মতো current রেখেই এইটা করছে।"),
    ],
    "Ch12Outro": [
        (3, "So here's what I'd like you to take",
         "So here's what I'd like you to take away. Every smaller transistor in this story had to do three "
         "things at once: turn off, still turn on with enough current, and fit into a cell you can build by "
         "the billion. The off state is the thread that kept coming back.",
         "তো যেটা আপনাদের সাথে নিয়া যাইতে বলবো: এই গল্পের প্রত্যেকটা ছোট transistor-রে একসাথে তিনটা কাজ করতে হইছে: off হওয়া, তবুও যথেষ্ট "
         "current নিয়া on হওয়া, আর billion-এ বানানো যায় এমন cell-এ আঁটা। Off অবস্থাটাই বারবার ফিরে আসা সুতা।"),
        (4, "And through all of it, one number",
         "And through all of it, k-T over q times ln 10, 59.5 millivolts per decade, is still the best an "
         "ordinary transistor can do at room temperature. Lab devices have crossed it. Making them useful and "
         "reliable, by the billion, is the next chapter.",
         "আর এর পুরাটা জুড়ে, k-T বাই q গুণ ln 10, প্রতি decade-এ 59.5 millivolt, এখনো room temperature-এ একটা সাধারণ transistor-এর সবচেয়ে "
         "ভালো। Lab-এর device এইটা পার হইছে। Billion-এর হিসাবে এগুলারে কাজের আর ভরসাযোগ্য বানানোই পরের chapter।"),
        (5, "Thank you. I'm happy to take",
         "Thank you. I'm happy to take questions.",
         "ধন্যবাদ। প্রশ্ন থাকলে করেন।"),
    ],
}

# The labs in the core, with shorter notes: (English, Bangla).
LABS = {
    "lab3_dennard.html": (
        "Live lab. Press Shrink 4 generations: sixteen times the transistors, each about four times as fast, "
        "and the same power density. Now press Voltage stuck, clock free: the same shrink, and the power "
        "density shoots up. That's the next chapter's problem.",
        "এইটা live lab। Shrink 4 generations চাপেন: ষোল গুণ transistor, প্রত্যেকটা প্রায় চার গুণ দ্রুত, আর একই power density। এবার "
        "Voltage stuck, clock free চাপেন: একই shrink, আর power density লাফ দিয়া বাড়ে। পরের chapter-এর সমস্যা এইটাই।"),
    "lab1_boltzmann.html": (
        "Live lab. Drag the gate voltage slowly up and watch electrons start to cross; the current climbs one "
        "decade for every 60 millivolts. Press 77 K: in this ideal model the swing gets four times steeper. "
        "Then raise m, the grip: the slope gets lazier.",
        "এইটা live lab। Gate voltage আস্তে আস্তে বাড়ান, দেখেন electron পার হওয়া শুরু করে; প্রতি 60 millivolt-এ current এক decade ওঠে। 77 K "
        "চাপেন: এই ideal model-এ swing চার গুণ খাড়া হয়। তারপর m, মানে grip, বাড়ান: slope ঢিলা হয়।"),
    "lab2_barrier.html": (
        "Live lab. A planar transistor with a 30 nanometre gate, about four and a half lambda: raise the drain "
        "voltage and watch the hill sink and the leakage climb. Now press FinFET: the same gate, and it's back "
        "in control.",
        "এইটা live lab। 30 nanometre gate-এর একটা planar transistor, প্রায় সাড়ে চার lambda: drain voltage বাড়ান, দেখেন hill নামে আর leakage "
        "বাড়ে। এবার FinFET চাপেন: একই gate, আবার control-এ।"),
    "lab4_cell.html": (
        "Live lab. Press Fewest tracks for each architecture: the FinFET needs seven tracks, the nanosheet six, "
        "the forksheet five, the CFET four, in these schematic models. Widen the sheets and watch the cell grow.",
        "এইটা live lab। প্রত্যেক architecture-এর জন্য Fewest tracks চাপেন: এই schematic model-গুলায় FinFET-এর সাতটা track লাগে, nanosheet-এর "
        "ছয়, forksheet-এর পাঁচ, CFET-এর চার। Sheet চওড়া করেন, দেখেন cell বড় হয়।"),
    "lab5_models.html": (
        "Live lab. FET Lab's own 3D models: drag to turn one, press Cut through the gate, and switch layers off "
        "to see the sheets inside.",
        "এইটা live lab। FET Lab-এর নিজের 3D model: টেনে ঘুরান, Cut through the gate চাপেন, আর layer বন্ধ করে ভিতরের sheet দেখেন।"),
}
