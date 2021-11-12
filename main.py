from nlplr.control.controller import TkEventController
from nlplr.analysis_NLP.analysis_options import AnalysisOption, AnalysisOptionsContainer

if __name__ == '__main__':
    # create the MVC & start the application
    c = TkEventController()

    analysis_options = AnalysisOptionsContainer()
    analysis_options.add_options([
        AnalysisOption(name='gram_lev', model='leven', preprocessing='processed_value', threshold=0.5),
        AnalysisOption(name='gram_lev2', model='leven', preprocessing='processed_value', threshold=0.3),
        AnalysisOption('sem_glove', 'open', 'glove_tokens', fn='calc_similarity_list', threshold=0.75),
        AnalysisOption('sem_glove2', 'open', 'glove_tokens', fn='calc_similarity_difference_list', threshold=0.8),
        AnalysisOption('sem_glove3', 'open', 'glove_tokens', fn='calc_combine_max_list', threshold=0.7),
        AnalysisOption('sem_spacy', 'spacy', 'spacy_tokens', fn='calc_similarity_list', threshold=0.75),
        AnalysisOption('sem_spacy', 'spacy', 'spacy_tokens', fn='calc_similarity_difference_list', threshold=0.8),
        AnalysisOption('sem_spacy2', 'spacy', 'spacy_tokens', fn='calc_combine_max_list', threshold=0.7)
    ])
        # self.analysis_options = [['leven', 'gram_lev', 'processed_value', '_'],
    #                          ['leven', 'gram_lev2', 'processed_value', '_'],
    #                          ['leven', 'gram_lev3', 'processed_value', '_'],
    #                          [['open', 'sem_glove', 'glove_tokens', 'calc_similarity_list'],
    #                           ['open', 'sem_glove2', 'glove_tokens', 'calc_similarity_difference_list'],
    #                           ['open', 'sem_glove3', 'glove_tokens', 'calc_combine_max_list']],
    #                          ['open', 'glove_final', 'glove_tokens', 'calc_combine_filter_list'],
    #                          [['spacy', 'sem_sp', 'spacy_tokens', 'calc_similarity_list'],
    #                           ['spacy', 'sem_sp2', 'spacy_lemmas', 'calc_similarity_difference_list'],
    #                           ['spacy', 'sem_sp3', 'spacy_lemmas', 'calc_combine_max_list']],
    #                          ['spacy', 'spacy_final', 'spacy_tokens', 'calc_combine_filter_list'],
    #                          ['leven', 'gram_final', 'processed_value', '_']]
    # self.analysis_thresholds = [0.5, 0.25, 0.15, [0.9, 0.8, 0.7], 0.5, [0.9, 0.8, 0.7], 0.5, 0.15]

    c.start(analysis_options=analysis_options)


