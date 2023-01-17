#############################  TO BPMN ##############################
from pm4py.objects.bpmn.obj import BPMN
from to_automaton import to_nfa_minimum_path_traces_occurrences, to_nfa_minimum_path, to_nfa_minimum_path_join_traces

def dfa_to_bpmn(dfa, remove_unnecessary_gateways=True,start_event_label="i_1"):
  bpmn = BPMN()
  start_event = BPMN.StartEvent(name=start_event_label, isInterrupting=True)
  bpmn.add_node(start_event)
  gateways = {}
  end_events = {}
  gateways_in = {}
  gateways_out = {}
  flows = {}
  for s in dfa.states:
    gateways[s] = BPMN.ExclusiveGateway(id=s, name=s)
    if remove_unnecessary_gateways:
      gateways_in[s] = []
      gateways_out[s] = []

  flow = BPMN.SequenceFlow(start_event, gateways[dfa.startState])
  bpmn.add_flow(flow)
  if remove_unnecessary_gateways:
    gateways_in[dfa.startState].append(start_event)
    flows[start_event, gateways[dfa.startState]] = flow    

  for s in dfa.acceptStates:
    end_events[s] = BPMN.EndEvent(name='e_'+s)
    flow = BPMN.SequenceFlow(gateways[s],end_events[s])
    bpmn.add_flow(flow)
    if remove_unnecessary_gateways:
      gateways_out[s].append(end_events[s])
      flows[gateways[s],end_events[s]] = flow    

  for s,a in dfa.transition:
    task = BPMN.Task(name=a)
    flow = BPMN.SequenceFlow(gateways[s], task)
    bpmn.add_flow(flow)
    if remove_unnecessary_gateways:
      gateways_out[s].append(task)
      gateways_in[dfa.transition[s,a]].append(task)
      flows[gateways[s], task] = flow    
    flow = BPMN.SequenceFlow(task, gateways[dfa.transition[s,a]])
    bpmn.add_flow(flow)
    if remove_unnecessary_gateways:
      flows[task, gateways[dfa.transition[s,a]]] = flow    

  if remove_unnecessary_gateways:
    for s in dfa.states:
      if(len(gateways_in[s])==1 and len(gateways_out[s])==1):
        s_in = gateways_in[s][0]
        s_out = gateways_out[s][0]
        bpmn.remove_flow(flows[s_in, gateways[s]])
        bpmn.remove_flow(flows[gateways[s], s_out])
        bpmn.add_flow(BPMN.SequenceFlow(s_in, s_out))
        bpmn.remove_node(gateways[s])

      if(len(gateways_in[s])==1 and len(gateways_out[s])==0):
        s_in = gateways_in[s][0]
        bpmn.remove_flow(flows[s_in, gateways[s]])
        bpmn.remove_node(gateways[s])

  return bpmn

def nfa_to_bpmn(nfa, remove_unnecessary_gateways=True):
  bpmn = BPMN()
  start_event = BPMN.StartEvent(name="i_1", isInterrupting=True)
  bpmn.add_node(start_event)
  gateways = {}
  end_events = {}
  gateways_in = {}
  gateways_out = {}
  flows = {}
  #Each state will be an exclusive gateway
  for s in nfa.states:
    gateways[s] = BPMN.ExclusiveGateway(id=s, name=s)
    if remove_unnecessary_gateways:
      gateways_in[s] = []
      gateways_out[s] = []

  #Adds the epsilon closure flows
  for s in nfa.states:
    for s_aux in nfa.epsilon_closure[s]:
      if s!=s_aux:
        flow = BPMN.SequenceFlow(gateways[s], gateways[s_aux])
        bpmn.add_flow(flow)
        if remove_unnecessary_gateways:
          gateways_in[gateways[s_aux]].append(gateways[s])
          gateways_out[gateways[s]].append(gateways[s_aux])
          flows[gateways[s], gateways[s_aux]] = flow    

  #Adds a flow from start event to gateway which represents the initial state.
  flow = BPMN.SequenceFlow(start_event, gateways[nfa.startState])
  bpmn.add_flow(flow)

  if remove_unnecessary_gateways:
    gateways_in[nfa.startState].append(start_event)
    flows[start_event, gateways[nfa.startState]] = flow    

  #For each accepting state, adds an end event
  for s in nfa.acceptStates:
    end_events[s] = BPMN.EndEvent(name='e_'+s)
    flow = BPMN.SequenceFlow(gateways[s],end_events[s])
    bpmn.add_flow(flow)
    if remove_unnecessary_gateways:
      gateways_out[s].append(end_events[s])
      flows[gateways[s],end_events[s]] = flow    


  for s,a in nfa.transition:
    if (a!=''):
      task = BPMN.Task(name=a)
      flow = BPMN.SequenceFlow(gateways[s], task)
      bpmn.add_flow(flow)
      if remove_unnecessary_gateways:
        gateways_out[s].append(task)
        flows[gateways[s], task] = flow    
      for n_s in nfa.transition[s,a]:
        flow = BPMN.SequenceFlow(task, gateways[n_s])
        bpmn.add_flow(flow)
        if remove_unnecessary_gateways:
          gateways_in[gateways[n_s]].append(task)
          flows[task, gateways[n_s]] = flow    

  if remove_unnecessary_gateways:
    for s in nfa.states:
      if(len(gateways_in[s])==1 and len(gateways_out[s])==1):
        s_in = gateways_in[s][0]
        s_out = gateways_out[s][0]
        bpmn.remove_flow(flows[s_in, gateways[s]])
        bpmn.remove_flow(flows[gateways[s], s_out])
        bpmn.add_flow(BPMN.SequenceFlow(s_in, s_out))
        bpmn.remove_node(gateways[s])

      if(len(gateways_in[s])==1 and len(gateways_out[s])==0):
        s_in = gateways_in[s][0]
        bpmn.remove_flow(flows[s_in, gateways[s]])
        bpmn.remove_node(gateways[s])

  return bpmn  

def traces_to_bpmn(lLog,remove_unnecessary_gateways=True):
  nfa = to_nfa_minimum_path(lLog)
  dfa = nfa.determinization().minimization()
  dfa.rename()

  return dfa_to_bpmn(dfa, remove_unnecessary_gateways=remove_unnecessary_gateways)


def traces_to_dfa(lLog):
  nfa = to_nfa_minimum_path(lLog)
  dfa = nfa.determinization().minimization()
  dfa.rename()

  return dfa


def traces_to_bpmn_join_traces(lLog,remove_unnecessary_gateways=True):
  nfa = to_nfa_minimum_path_join_traces(lLog)
  dfa = nfa.determinization().minimization()
  dfa.rename()

  return dfa_to_bpmn(dfa, remove_unnecessary_gateways=remove_unnecessary_gateways)

def traces_to_dfa_join_traces(lLog):
  nfa = to_nfa_minimum_path_join_traces(lLog)
  dfa = nfa.determinization().minimization()
  dfa.rename()

  return dfa

def traces_to_dfa_traces(traces,traces_indices):
  nfa = to_nfa_minimum_path_traces_occurrences(traces,traces_indices)
  dfa = nfa.determinization().minimization()
  dfa.rename()

  return dfa

def traces_to_bpmn_traces(traces,traces_indices,remove_unnecessary_gateways=True):
  dfa = traces_to_dfa_traces(traces,traces_indices)
  return dfa_to_bpmn(dfa, remove_unnecessary_gateways=remove_unnecessary_gateways)
