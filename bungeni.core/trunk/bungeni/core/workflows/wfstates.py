# encoding: utf-8

#central storage for workflow states


from bungeni.core.i18n import _

class questionstates:
    draft = _(u"draft question") # a draft question of a MP
    private = _("private question") # private draft of a MP
    submitted = _(u"Question submitted to clerk") # submitted from MP to clerks office
    received = _(u"Question received by clerk") # recieved by clerks office
    complete = _(u"Question complete") # reviewed by clers office sent to speakers office
    admissible = _(u"admissible Question") # reviewed by speakers office available for scheduling or to
                                  # to be send to ministry for written response
    inadmissible = _(u"inadmissible Question") # rejected by speakers office
    clarify_mp = _(u"Question needs MP clarification") # clerks office needs clarification by MP
    clarify_clerk = _(u"Question needs Clerks clarification") # speakers office needs clarification by clerks office
    scheduled =_(u"Question scheduled") # is scheduled for debate at a sitting
    response_pending = _(u"Question pending response") # ministry has to write a response
    deferred = _(u"Question deferred") # admissable question that cannot be debated 
    postponed = _(u"Question postponed") # question was scheduled for but not debated at the sitting
    elapsed = _(u"Question elapsed") # defered or postponed question that were not answered
                            # or questions that required a written answer by a ministry which were not answered
    responded = _(u"Question responded") # a question was debated or a written answer was given by a ministry
    answered = _(u"Question answered") # the written answer was reviewed by the clerks office
                              # or debate reference input by clerks office
    withdrawn = _(u"Question withdrawn") # the owner of the question can withdraw the question


class responsestates:
    draft = _(u"draft response") # a draft response of a Ministry
    submitted = _(u"response submitted") # response submitted to clerks office for review
    complete = _(u"response complete") # response reviewed by clerks office


class billstates:

    draft = _(u"draft bill")
    #member_draft = "member_draft"
    
    submitted = _(u"bill published in gazette")
    first_reading = _(u"first reading")
    first_reading_postponed = _(u"first reading postponed")
    first_committee = _(u"first committee")

    # after a committee, there is an option to
    # present the finding directly to the house.
    # report_reading_1 = "report_reading_1"
    
    # to be scheduled for 2nd reading
    second_reading_pending = _(u"second reading pending")
    second_reading = _(u"second reading")
    second_reading_postponed = _(u"second reading postponed")

    # to be scheduled for whole house
    house_pending = _(u"house pending")
    whole_house =_(u"whole house")
    whole_house_postponed =_(u"whole house postponed")

    second_committee = _(u"second committee")

    # to be scheduled for report reading
    report_reading_pending = _(u"report reading pending")
    report_reading = _(u"report reading")
    report_reading_postponed = _(u"report reading postponed")


    # is there a third pending state for a bill
    third_reading_pending = _(u"third reading pending")
    third_reading = _(u"third reading")
    third_reading_postponed = _(u"third reading postponed")

    withdrawn = _(u"bill withdrawn")

    approved = _(u"approved")
    rejected = _(u"rejected")
    
class motionstates:
    draft = _(u"draft motion") # a draft motion of a MP
    private = _("private motion") # private draft of a MP
    submitted = _(u"Motion submitted") # submitted from MP to clerks office
    received = _(u"Motion received by clerks office") # recieved by clerks office
    complete = _(u"Motion complete") # reviewed by clers office sent to speakers office
    admissible = _(u"Motion admissible") # reviewed by speakers office available for scheduling
    inadmissible = _(u"Motion inadmissible") # rejected by speakers office
    clarify_mp = _(u"Motion needs clarification by MP") # clerks office needs clarification by MP
    clarify_clerk = _("Motion needs clarification by Clerks Office") # speakers office needs clarification by clerks office
    scheduled =_(u"Motion scheduled") # is scheduled for debate at a sitting
    deferred = _(u"Motion deferred") # admissable motion that cannot be debated 
    postponed = _(u"Motion postponed") # motion was scheduled for but not debated at the sitting
    elapsed = _(u"Motion elapsed") # defered or postponed motion that were not debated
    debated = _(u"Motion debated") # a motion was debated 
    withdrawn = _(u"Motion withdrawn") # the owner of the motion can withdraw the motion    
