from teocomp.nfa_e import NFA_E

def removeAllSequencesOfRepetitions(l):
    indexes_repetitions = []
    b = True
    while b:
        b = False
        rep = 0
        for i in range(len(l)):
            rep = 0
            nexts = []
            for k in range(i+1,len(l)):
                if l[i]==l[k]: nexts.append(k)
            for j in nexts:
                size = j-i
                while(l[i:j]==l[j+rep*size : j+rep*size+size]):
                    rep += 1
                if rep>0:
                    l = l[:j]+l[j+rep*size:]
                    # Atualiza os indices                    
                    #Cria os novos indices
                    new_indexes_repetitions  = []
                    # Adiciona a repetição na nova sequência
                    new_indexes_repetitions.append([i,j-1])    
                    for ir in indexes_repetitions:
                        ir0 = ir[0]
                        ir1 = ir[1]
                        size_deleted_sequence = rep*size
                        
                        if(ir0>j-1):
                            if(ir0 > i+size_deleted_sequence): 
                                ir0 = ir0 - size_deleted_sequence
                            else:
                                ir0 = i+ ((ir0-i) % size) 
                        if(ir1>j-1):
                            if(ir1 > i+size_deleted_sequence): 
                                ir1 = ir1 - size_deleted_sequence
                            else:
                                ir1 = i+ ((ir1-i) % size) 
                        new_indexes_repetitions.append([ir0,ir1])
                    indexes_repetitions = new_indexes_repetitions
                    break
            if rep>0 :
                b = True
                break
    return l,indexes_repetitions


def to_nfa(lLog, prefix_name="s"):

    """ Convert a list of traces (logs) as a NFA.

    :param: List of Traces (e.g. [ ['a','b'], ['a','b','e'], ['a','e'] ]);
    :return: *(dict)* representing a NFA.
    """
    states = set()
    accepting_states = set()
    alphabet = set()
    transitions = {}  # key [state ∈ states, action ∈ alphabet]
    #                   value [arriving state ∈ states]

    initial_state = prefix_name+'0'
    states.add(initial_state)
    i = 1
    for j in range(len(lLog)):
        for k in range(len(lLog[j])):
            states.add(prefix_name+str(i))
            if(k==len(lLog[j])-1):
                accepting_states.add(prefix_name+str(i))
            alphabet.add(lLog[j][k])
           
            if(k==0):
                transitions.setdefault((prefix_name+'0', lLog[j][k]), set()).add(prefix_name+str(i))
            else:
                transitions.setdefault((prefix_name+str((i-1)), lLog[j][k]), set()).add(prefix_name+str(i))
            i += 1

    return NFA_E(states,alphabet,initial_state,transitions,accepting_states)



def to_nfa_history(lLog, history=-1):

    """ Convert a list of traces (logs) as a NFA, regarding the history of events.

    :param: List of Traces (e.g. [ ['a','b'], ['a','b','e'], ['a','e'] ]);
    :return: *(dict)* representing a NFA.
    """
    states = set()
    initial_states = set()
    accepting_states = set()
    alphabet = set()
    transitions = {}  # key [state ∈ states, action ∈ alphabet]
    #                   value [arriving state ∈ states]

    initial_state = '[]'
    states.add(initial_state)
    for j in range(len(lLog)):
        inicio = 0
        state_inicio = '[]'
        for k in range(len(lLog[j])):            
            if(history>0 and history <= k): inicio = k+1-history
            state_prox = '['+','.join(lLog[j][inicio:k+1])+']'
            states.add(state_prox)
            
            if(k==len(lLog[j])-1):
                #accepting_states.add(str())
                accepting_states.add(state_prox)
            alphabet.add(lLog[j][k])            
            transitions.setdefault((state_inicio, lLog[j][k]), set()).add(state_prox)           
            state_inicio = state_prox

    return NFA_E(states,alphabet,initial_state,transitions,accepting_states)


def to_nfa_minimum_path(lLog,prefix_name="s", rework=True):

    """ Convert a list of traces (logs) as a NFA.

    :param: List of Traces (e.g. [ ['a','b'], ['a','b','e'], ['a','e'] ]);
    :return: *(dict)* representing a NFA.
    """
    states = set()
    accepting_states = set()
    alphabet = set()
    transitions = {}  # key [state ∈ states, action ∈ alphabet]
    #                   value [arriving state ∈ states]

    initial_state = prefix_name+'0'
    states.add(initial_state)
    i = 1 # state
    for j in range(len(lLog)):
        pos_i = i
        trace, trace_new_transitions = removeAllSequencesOfRepetitions(lLog[j])
        for k in range(len(trace)):
            states.add(prefix_name+str(i))
            if(k==len(trace)-1):
                accepting_states.add(prefix_name+str(i))
            alphabet.add(trace[k])
           
            if(k==0):
                transitions.setdefault((prefix_name+'0', trace[k]), set()).add(prefix_name+str(i))
            else:
                transitions.setdefault((prefix_name+str((i-1)), trace[k]), set()).add(prefix_name+str(i))
            i += 1
        if rework:
            for t in trace_new_transitions:
                pos_dest = pos_i + t[1] 
                if (t[0]==0): 
                    transitions.setdefault((prefix_name+'{}'.format(pos_dest), ''), set()).add(prefix_name+'0')
                else:
                    pos_ini = pos_i+t[0]-1
                    transitions.setdefault((prefix_name+'{}'.format(pos_dest), ''), set()).add(prefix_name+'{}'.format((pos_ini)))

    return NFA_E(states,alphabet,initial_state,transitions,accepting_states)

def to_nfa_minimum_path_join_traces(lLog,prefix_name="s", rework=True):

    """ Convert a list of traces (logs) as a NFA.

    :param: List of Traces (e.g. [ ['a','b'], ['a','b','e'], ['a','e'] ]);
    :return: *(dict)* representing a NFA.
    """
    states = set()
    accepting_states = set()
    alphabet = set()
    transitions = {}  # key [state ∈ states, action ∈ alphabet]
    #                   value [arriving state ∈ states]

    initial_state = prefix_name+'0'
    states.add(initial_state)
    traces = []
    traces_indices = []
    for j in range(len(lLog)):
        trace, trace_new_transitions = removeAllSequencesOfRepetitions(lLog[j])
        if trace in traces:
          if rework:
            for i in range(len(traces)):
                if trace == traces[i]: 
                    for t_n_t in trace_new_transitions:
                        if not t_n_t in traces_indices[i]:
                            traces_indices[i].append(t_n_t)
        else:
          traces.append(trace)
          if rework:
              traces_indices.append(trace_new_transitions)

    i = 1 # state
    for j in range(len(traces)):
        pos_i = i
        trace = traces[j]
        trace_new_transitions = traces_indices[j]
        for k in range(len(trace)):
            states.add(prefix_name+str(i))
            if(k==len(trace)-1):
                accepting_states.add(prefix_name+str(i))
            alphabet.add(trace[k])
           
            if(k==0):
                transitions.setdefault((prefix_name+'0', trace[k]), set()).add(prefix_name+str(i))
            else:
                transitions.setdefault((prefix_name+str((i-1)), trace[k]), set()).add(prefix_name+str(i))
            i += 1
        if rework:
            for t in trace_new_transitions:
                pos_dest = pos_i + t[1] 
                if (t[0]==0): 
                    transitions.setdefault((prefix_name+'{}'.format(pos_dest), ''), set()).add(prefix_name+'0')
                else:
                    pos_ini = pos_i+t[0]-1
                    transitions.setdefault((prefix_name+'{}'.format(pos_dest), ''), set()).add(prefix_name+'{}'.format((pos_ini)))

    return NFA_E(states,alphabet,initial_state,transitions,accepting_states)


def get_occurrences(dfa, lLog):
    s = dfa.startState
    new_transitions = dict()
    for (s,a) in dfa.transition:
        new_transitions[s,a] = 0
    for l in lLog:
        s = dfa.startState
        for a in l:
            if (s,a) in dfa.transition:
                new_transitions[s,a] = new_transitions[s,a]+1
                s = dfa.transition[s,a]
    return new_transitions

def add_occurrences_to_label(dfa, lLog):
    occurrences = get_occurrences(dfa, lLog)
    new_transitions = dict()
    for (s,a) in dfa.transition:
        new_transitions[s, f'{a} ({occurrences[s,a]})'] = dfa.transition[s,a]
    dfa.transition = new_transitions

def remove_occurrences(dfa, lLog, size=0):
    occurrences = get_occurrences(dfa, lLog)
    new_transitions = dict()
    for (s,a) in dfa.transition:
        if occurrences[s,a]>=size:
            new_transitions[s, a] = dfa.transition[s,a]
    dfa.transition = new_transitions

def set_occurrences(dfa, lLog, size=0):
    remove_occurrences(dfa, lLog, size)
    dfa.remove_unreachable_states()
    add_occurrences_to_label(dfa, lLog)



def to_nfa_minimum_path_traces_occurrences(traces, traces_indices,prefix_name="s"):

    """ Convert a list of traces (logs) as a NFA.

    :param: List of Traces (e.g. [ ['a','b'], ['a','b','e'], ['a','e'] ]);
    :return: *(dict)* representing a NFA.
    """
    states = set()
    accepting_states = set()
    alphabet = set()
    transitions = {}  # key [state ∈ states, action ∈ alphabet]
    #                   value [arriving state ∈ states]

    initial_state = prefix_name+'0'
    states.add(initial_state)
    # traces = []
    # traces_indices = []
    # for j in range(len(lLog)):
    #     trace, trace_new_transitions = removeAllSequencesOfRepetitions(lLog[j])
    #     if trace in traces:
    #       for i in range(len(traces)):
    #         if trace == traces[i]: 
    #           for t_n_t in trace_new_transitions:
    #             if not t_n_t in traces_indices[i]:
    #               traces_indices[i].append(t_n_t)
    #     else:
    #       traces.append(trace)
    #       traces_indices.append(trace_new_transitions)

    i = 1 # state
    for j in range(len(traces)):
        pos_i = i
        trace = traces[j]
        trace_new_transitions = traces_indices[j]
        for k in range(len(trace)):
            states.add(prefix_name+str(i))
            if(k==len(trace)-1):
                accepting_states.add(prefix_name+str(i))
            alphabet.add(trace[k])
           
            if(k==0):
                transitions.setdefault((prefix_name+'0', trace[k]), set()).add(prefix_name+str(i))
            else:
                transitions.setdefault((prefix_name+str((i-1)), trace[k]), set()).add(prefix_name+str(i))
            i += 1
        for t in trace_new_transitions:
            pos_dest = pos_i + t[1] 
            if (t[0]==0): 
                transitions.setdefault((prefix_name+'{}'.format(pos_dest), ''), set()).add(prefix_name+'0')
            else:
                pos_ini = pos_i+t[0]-1
                transitions.setdefault((prefix_name+'{}'.format(pos_dest), ''), set()).add(prefix_name+'{}'.format((pos_ini)))

    return NFA_E(states,alphabet,initial_state,transitions,accepting_states)



