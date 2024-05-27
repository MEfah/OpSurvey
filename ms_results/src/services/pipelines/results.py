def get_result_pipeline(survey_id: str) -> list[dict]:
    """Получить пайплайн для получения агрегированной информации о результатах"""
    return [
      { 
        "$match": { 
          "survey_id": survey_id,
          "is_finished": True
        }
      },
      {
        "$unwind": "$question_answers"
      },
      {
        "$project": {
          "_id": "$question_answers.id",
          "value": "$question_answers.value",
          "options": "$question_answers.options"
        }
      },
      {
        "$facet": {
          "number_questions": [
            {
              "$match": {
                "$and": [
                  {"options": {"$exists": False}},
                  { "value": {"$type": "number"}}
                ]
              }
            },
            {
              "$group": {
                "_id": "$_id",
                "answer_count": {"$count": {}},
                "mean": { "$avg": "$value"},
                "min": { "$min": "$value"},
                "max": { "$max": "$value"},
                "values": { "$push": "$value"},
              }
            },
            {
              "$addFields": {
                "step": {
                  "$divide": [{"$subtract": ["$max", "$min"]}, {"$add": [{"$floor": {"$log": ["$answer_count", 2]}}, 1]}]
                }
              }
            },
            {
              "$unwind": "$values"
            },
            {
              "$addFields": {
                "interval_from": {
                  "$subtract": ["$values", {"$mod": [{"$subtract": ["$values", "$min"]}, "$step"]}]
                }
              }
            },
            {
              "$group": {
                "_id": {"id": "$_id", "interval_from": "$interval_from"},
                "min": {"$first": "$min"},
                "max": {"$first": "$max"},
                "mean": {"$first": "$mean"},
                "answer_count": {"$first": "$answer_count"},
                "interval_count": {"$count": {}}
              }
            },
            {
              "$group": {
                "_id": "$_id.id",
                "min": {"$first": "$min"},
                "max": {"$first": "$max"},
                "mean": {"$first": "$mean"},
                "answer_count": {"$first": "$answer_count"},
                "intervals": {
                  "$push": {
                    "from": "$_id.interval_from",
                    "count": "$interval_count"
                  }
                }
              }
            }
          ],
          "date_questions": [
            {
              "$match": {
                "$and": [
                  {"options": {"$exists": False}},
                  { "value": {"$type": "date"}}
                ]
              }
            },
            {
              "$addFields": {
                "value": {
                  "$convert": {
                    "input": "$value",
                    "to": "long"
                }}
              }
            },
            {
              "$group": {
                "_id": "$_id",
                "answer_count": {"$count": {}},
                "mean": { "$avg": "$value"},
                "min": { "$min": "$value"},
                "max": { "$max": "$value"},
                "values": { "$push": "$value"},
              }
            },
            {
              "$addFields": {
                "step": {
                  "$divide": [{"$subtract": ["$max", "$min"]}, {"$add": [{"$floor": {"$log": ["$answer_count", 2]}}, 1]}]
                }
              }
            },
            {
              "$unwind": "$values"
            },
            {
              "$addFields": {
                "interval_from": {
                  "$convert": {"input": {"$subtract": ["$values", {"$mod": [{"$subtract": ["$values", "$min"]}, "$step"]}]}, "to": "date"}
                  
                }
              }
            },
            {
              "$group": {
                "_id": {"id": "$_id", "interval_from": "$interval_from"},
                "min": {"$first": "$min"},
                "max": {"$first": "$max"},
                "mean": {"$first": "$mean"},
                "answer_count": {"$first": "$answer_count"},
                "interval_count": {"$count": {}}
              }
            },
            {
              "$group": {
                "_id": "$_id.id",
                "min": {"$first": "$min"},
                "max": {"$first": "$max"},
                "mean": {"$first": "$mean"},
                "answer_count": {"$first": "$answer_count"},
                "intervals": {
                  "$push": {
                    "from": "$_id.interval_from",
                    "count": "$interval_count"
                  }
                }
              }
            },
            {
              "$addFields": {
                "min": {
                  "$convert": {
                    "input": "$min",
                    "to": "date"
                }},
                "max": {
                  "$convert": {
                    "input": "$max",
                    "to": "date"
                }},
                "mean": {
                  "$convert": {
                    "input": "$mean",
                    "to": "date"
                }}
              }
            },
          ],
          "options_questions": [
            {
              "$match": {
                "$and": [
                  {"options": {"$exists": True}}
                ]
              }
            },
            {
              "$group": {
                "_id": "$_id",
                "options": {"$push": "$options"},
                "answer_count": {"$count": {}}
              }
            },
            {
              "$unwind": {
                "path": "$options",
                "preserveNullAndEmptyArrays": True
              }
            },
            {
              "$unwind": {
                "path": "$options",
                "preserveNullAndEmptyArrays": True
              }
            },
            {
              "$group": {
                "_id": {"question_id": "$_id", "option_id": "$options"},
                "answer_count": {"$first": "$answer_count"},
                "count": { "$count": {}},
              }
            },
            {
              "$group": {
                "_id": "$_id.question_id",
                "answer_count": {"$first": "$answer_count"},
                "options": {
                  "$push": {
                    "id": "$_id.option_id",
                    "count": "$count"
                  }
                }
              }
            }
          ],
          "string_questions": [
            {
              "$match": {
                "$and": [
                  {"options": {"$exists": False}},
                  { "value": {"$type": "string"}}
                ]
              }
            },
            {
              "$group": {
                "_id": "$_id",
                "answer_count": {"$count": {}}
              }
            },
          ]
        }
      },
      {
        "$project": {
          "value_results": { "$concatArrays": ["$number_questions", "$date_questions", "$string_questions"]},
          "options_results": "$options_questions"
        }
      }
    ]