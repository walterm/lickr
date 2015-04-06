Lickr.Question = DS.Model.extend({
    text: DS.attr('string'),
    image1: DS.attr('string'),
    image2: DS.attr('string')
});

Lickr.Question.FIXTURES = [
    {
        id: 1,
        text: "question 1",
        image1: "mock1.jpg",
        image2: "mock2.jpg",
        image3: "mock3.jpg",
        image4: "mock4.jpg"
    },
    {
        id: 2,
        text: "question 2",
        image1: "mock1.jpg",
        image2: "mock2.jpg",
        image3: "mock3.jpg",
        image4: "mock4.jpg"
    },
    {
        id: 3,
        text: "question 3",
        image1: "mock1.jpg",
        image2: "mock2.jpg",
        image3: "mock3.jpg",
        image4: "mock4.jpg"
    },
    {
        id: 4,
        text: "question 4",
        image1: "mock1.jpg",
        image2: "mock2.jpg",
        image3: "mock3.jpg",
        image4: "mock4.jpg"
    }
];