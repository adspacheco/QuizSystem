from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.generics import (ListAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     CreateAPIView,
                                     RetrieveAPIView,
                                     )
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTeacher, IsTeacherOrReadOnly, IsTeacherOrIsStudentReadOnly, StudentReadOnly
from homework.models import Quiz, Question, Course, GradedQuiz, Choice
from users.models import User, Teacher, Student
from users.serializers import StudentSerializer
from .serializers import (QuizSerializer,
                          QuestionSerializer,
                          CourseSerializer,
                          CourseAllSerializer,
                          GradedQuizSerializer,
                          ChoiceSerializer)
from users.serializers import UserSerializer


# User Details
class CurrentUserView(RetrieveAPIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# Course Query Views

class AllCourseListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CourseAllSerializer
    queryset = Course.objects.all().order_by('-created_at')


class CourseListView(ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        Returns the list of courses the signed in teacher teaches or student takes
        """
        user = self.request.user
        if user.role == "ST":
            return Course.objects.filter(students__user=user).order_by('-created_at')
        elif user.role == "TE":
            return Course.objects.filter(teacher=user).order_by('-created_at')


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class CourseCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacher, )
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


# Quiz Query Views
class QuizListView(ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
        Returns the list of courses a teacher teaches
        """
        courseID = self.kwargs['courseID']
        return Quiz.objects.filter(course__pk=courseID).order_by('-created_at')


class QuizDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsTeacherOrReadOnly, )
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


class QuizCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacher, )
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


# GradedQuiz Views


class GradedQuizListView(ListAPIView):
    serializer_class = GradedQuizSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return GradedQuiz.objects.filter(student=user).order_by('created_at')


class GradedQuizCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = GradedQuizSerializer
    queryset = GradedQuiz.objects.all()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

# Question Views


class QuestionCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacher, )
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

# Choice Views


class ChoiceCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacher, )
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()


# Student Views

class StudentDetailView(RetrieveUpdateDestroyAPIView):
    permissions = (IsAuthenticated, StudentReadOnly, )
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk')

        if pk == "current":
            pk = self.request.user.pk
            return Student.objects.filter(user__pk=pk).first()

        return super(StudentDetailView, self).get_object()
