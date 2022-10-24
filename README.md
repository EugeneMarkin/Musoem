#### Velemere Intro

Velemere is a meta-language for real-time algorithmic composition and performance. In other words, it a is tool for *live coding* using the natural language. Unlike other live coding languages which consist of operators and functions, Velemere operates with ***keywords***. Keywords are simply *words* (or *strings* in programming terms) that you assign to sections of your music or to chosen algorithmic transformations of that music. The tool is designed to be used along with the common music notation software, allowing the real-time algorithmic manipulations of a pre-composed score. Velemere is written in Python and uses *FoxDot* - a live coding language with rich functionality and *music21* - a library for computer-aided musicology. This allows the user to explore full potential of these two libraries when designing algorithmic music processes, deconstructing the score or improvising with code. 

#### Features

- ​	**MusicXML file import/export.** For the music that largely works with pitch and rhythm it is often convenient to use common western notation, rather than writing lists of numbers in the code to notate these musical features. Instead of writing large FoxDot patterns in the code editor, simply import the score from a MusicXML file. Velemere has a set of functions for creating patterns out of sections of the score or individual measures. The resulting objects are calles ***Sections*** and contain within them patterns of pitch, duration, velocity and tempo that can all be manipulated with FoxDot. Additionally, sections can be sequenced, combined, delayed or repeated a finite number of times, which gives you presice control over the scheduling of musical events. This creates a possibility to perform pieces with live coding that do not necessarily suggest a repetitive structure, but can have any form and express many compositional ideas. It may be especially useful for composing mixed music pieces for live coding and acoustic instruments. The results of the algorithmic manipulations can be saved back to MusicXML format and then edited in any software of choise. 
- **Control operations.** In computer music it is often desired to apply transformations to the sound parameters regardless of the particular rhythm/pitch pattern that is currently playing. Velemere adds standalone **Control** objects to FoxDot, which allow you to quickly execute gradual/periodic changes in timbre of individual instruments or the entire digital ensemble. 
- **Live coding in natural language.**  Live coding performance requires a substantial knowlegde of a partucular programming language, its syntax and functions. Since there are already many languages used by live coders, it is unrealistic to expect the audience to understand the thought process happening on screen beyond basic action/reaction comprehension. Velemere lets the user design "their own language" that would both suit their musical intensions and be meaninful to the audience in the ceratain way. The **keywords** for score sections can be added as simple text above the staves right into the score. Keywords for control operations and score transformations are assigned in the mapping text file, where the user can choose from a number of pre-defined functions or create their own. A set of default mappings for common operations such as "and", "or" and others is available, but can be redefined if needed. 
- **Customizable gui console for performance**.  Because it is crucial in a live coding performance to display the screen with code, the visual aspect is the integral part of the practice. Velemere attempts to break away from the "looking at the code" paradigm, enabling broader artistic choises of the visual representation. The console window is divided into two sections: input and output - both displaying plain text. The input section is used for typing sentences that are interpreted as commands for the music engine to play patterns and apply operations. The currently playing patterns and operations (expressed by their keywords) are displayed in the output window also as plain text. The user may alter what is currently playing by simply editing the text in the output window. The background of the window may be an image or a video that the artist chooses. The current state of the background may be assigned to the keywords as well, and be used for example to display the parts of the score or any graphics that suit the aesthetics of the piece. 

#### Documentation

##### User interface. 

- Input console.

  - Ctrl + Enter. Evaluate single line (sentence). The line will be parsed as a command and executed immediately.
  - Multi-line input. Select multiple lines of code and evaluate with ctrl + enter. Each line will be parsed as a command and the commands will be sequenced.
  - Window menu: change the font, text color, background color, background image or video.

- Output console.

  The parsed sentenses that are currently playing are displayed in the window in the following format:

  - Section keyword followed by the operations currenly applied to the section, divided by single space.
  - Each section is displayed in the new line. 
  - Control operations are displayed in the last line.

  To stop a playing section, section operation or control operation, delete a keyword or multiple keywords and press ctrl + enter.

**Language.**

- Basic parsing rules: 

  - `section1 section2`  - sequences sections 1 and 2

  - `section1 operation1 section2 operation2` - applies *operation1* to *section1*, applies *operation2* to *section2*, sequences sections. 

    > **Note**: sections and operations are parse separately, so only the order of the elements of the same type matters. For example:
    >
    > `section1 operation1 operation2 section2` will give the same result.
    >
    > `section1 section2 operation2 operation1` - applies *operation2* to *section1* and *operation1* to *section2*. 

  - `section1 section2 operation1` - applies *operation1* to both sections 1 and 2, sequences sections 

    > **Note**: if section1 is already playing, this code will apply operation1 to section2 only and sequence it to play after section 1 without interrupting section 1

  - `section1 operation1 operation2 `- applies both operations to *section1*, plays *section1*

  - `section1 operation1 control1 control2` - applies operation1 to section1, plays section1 and starts control operations 1 and 2.

  - `section <some_word> operation` - any words in the text that are not keywords are ignored. 

  > **Example 1**: 
  >
  > Suppose we have the following keywords: 
  >
  >   **Michael** - 2 quarter notes of pitches C4 and E4. 
  >   **row** - a dotted quarter note of pitch G4
  >   **boat** - 8th E4 followed by quarter G4 and A4
  >   **ashore** - a pattern operation which swaps the first and last notes of the pattern.
  >   **Halleluja** - speeds up the global clock tempo to 200 bpm over 4 beats
  >
  >   then the following line: 
  >
  > `Michael row the boat ashore, Halleluja` - will play this line (TODO: add image) with an accelerando from the current tempo and up to 200 bpm in the first repetition and then will keep playing the pattern at 200 bpm until it is stopped. 
  >
  > The output window display will look like:
  >
  > ```
  > Michael ashore
  > Halleluja
  > ```
  >
  > Then 
  >
  > ```
  > row ashore 
  > Halleluja
  > ```
  >
  > Then 
  >
  > ```
  > boat ashore
  > Halleluja
  > ```
  >
  > Deleting the word "ashore" at any stage will reset the section to its original state.
  >
  > Deleting the word "Michael" or "row" or "boat" will stop the section and will **not** play any sections that were sequenced after it.
  >
  > Deleting the word Halleluja will instantly set the tempo back to its original value.

  

- **Comma** - Sequence events.

  - `section1, section2, section3 operation1` - applies operation1 to section3, sequences sections 1,2,3

  - `section1, section2, section3, operation1, operation2` - sequence sections 1, 2, 3, apply both operations to the section 1.

    > Note: At the moment, all the section operations take 1 section as an argument. So no operations on multiple sections are possible. This is done to keep the language as "natural" as possible while preserving some clarity of the logic behind parsing of sentenses.

  - `section1, section2 section3 operation1, control1` - applies operation 1 to section2 and 3, sequences sections 1,2,3 and after section3 is finished starts control1 operation (**TODO: implement this**)

- Special keywords:

  - **and**, **with** (duplicated with "&)": TODO: implement "&" duplication 
    - ` section1 and section2 operation1 operation2` - applies operation1 to section1, operation2 to section2 and plays both sections at the same time
    - `section1 section2 operation1 and operation2` - applies both operations to both sections and plays them at the same time
    - `section1 and section2 and section3 operation1` - applies operation 1 to section 3 and then plays all three sections together.
  - **or** - random choise.
    - `section1 or section2 operation1` - plays either section1 or 2 with operation 1 applied
    - `section1 operation1 or operation2`- applies either operation 1 or 2 to section 1, plays section1
    - `section1 or section2 or operation1` - this will either play section1 or section2, or will play neither of them and apply operation1 to the currently playing section (the last in the list).
    - `section1 or operation1 or control1` - will either play section1 or apply opeartion1 to currently playing section, or trigger control1.
    - `section1 and section2 or section3 operation1` - will play section1 and either section2 or section3. If section3 is played then operation1 will be applied to it, otherwise operation1 is not applied to anything
  - **not,  don't, isn't, doesn't, stop, quit, cancel** - stop section or operation.
    - `section1 not operation1 ` - resets operation1 from section1
    - `section2 isn't section1 and not operation1` - start section2, stop section1. In case section 2 is already playing this will stop operation1 on that section.

  ​	

- Punctuation marks in the end of the sentence:

  - No mark - play resulting pattern on repeat
  - "." - play pattern once, "..." - play pattern 3 times
  - "!" - play  pattern with crescendo
  - "?" - play pattern with diminuendo

  Example

  `lorem ipsum dolor sit amet!!!` - play pattern 3 times with cresecendo

- Default section operations. (Can be overriden)

  - **some**, **a little**, **a bit** TODO

  - **more**, **less** TODO

  - **kind of**, **sort of**, **like**

  - **opposite**, 

  - **quicker**, **slower**

  - **higher, lower**

    



Velemere adds a higher level of abstration to FoxDot. When improvising with algorithmic operations on your music, you may not wish think about which mathematical operations you should apply to which patterns of pitch, duration or velocity. Velemere provides a set of functions that aim at having certain "musical" meaning. The input parameters to these functions can be passed in the brackets after each function, e.g. transpose(12) - will transpose the section up an octave. So when you are rehearsing your performance, trying out different operations that may work for a particular piece, you can easily expore posisble options. In a concert situation, you may pin those parameters and assign keywords to each specific operations. For example transpose(12) may be called "elevate" and transpose(-7) may be called "descent" so that the connection between the text on screen and its effect on music would be evident to any listener, regardless of their musical background.

