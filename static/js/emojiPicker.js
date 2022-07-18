for (let i = 1; i < 6; i++) {
            let selector="emoji-selector-" + i;
            document.getElementsByClassName(selector)[0].addEventListener('click', (e) => {
                console.log('click');
                let selectorNumber = e.target.dataset.number;
                let emojiInput = "emoji-input-" + selectorNumber;
                console.log(emojiInput);
                document.getElementsByClassName(emojiInput)[0].value = "";
        });
        }

        
        new EmojiPicker({
            trigger: [
                {
                    selector: '.emoji-selector-1',
                    insertInto: '.emoji-input-1'
                },
                {
                    selector: '.emoji-selector-2',
                    insertInto: '.emoji-input-2'
                },
                {
                    selector: '.emoji-selector-3',
                    insertInto: '.emoji-input-3'
                },
                {
                    selector: '.emoji-selector-4',
                    insertInto: '.emoji-input-4'
                },
                {
                    selector: '.emoji-selector-5',
                    insertInto: '.emoji-input-5'
                }
            ],
            closeButton: true,
        });